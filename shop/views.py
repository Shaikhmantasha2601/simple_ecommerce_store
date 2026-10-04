from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm, RegisterForm
from .models import Order, OrderItem, Product


def _cart_data(request):
    cart = request.session.get("cart", {})
    products = Product.objects.filter(id__in=cart.keys()) if cart else Product.objects.none()

    items = []
    total = Decimal("0.00")

    for product in products:
        quantity = int(cart.get(str(product.id), 0))
        if quantity <= 0:
            continue
        subtotal = product.price * quantity
        total += subtotal
        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    return items, total


def home(request):
    products = Product.objects.all()
    category = request.GET.get("category", "")
    query = request.GET.get("q", "").strip()

    if category:
        products = products.filter(category=category)
    if query:
        products = products.filter(name__icontains=query)

    categories = Product.objects.values_list("category", flat=True).distinct()
    return render(request, "shop/home.html", {
        "products": products,
        "categories": categories,
        "selected_category": category,
        "query": query,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "shop/product_detail.html", {"product": product})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.stock <= 0:
        messages.error(request, "This product is currently out of stock.")
        return redirect("product_detail", pk=pk)

    quantity = max(int(request.POST.get("quantity", 1)), 1)
    cart = request.session.get("cart", {})
    current = int(cart.get(str(pk), 0))
    cart[str(pk)] = min(current + quantity, product.stock)
    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to your cart.")
    return redirect(request.POST.get("next", "cart"))


def cart_view(request):
    items, total = _cart_data(request)
    return render(request, "shop/cart.html", {"items": items, "total": total})


def update_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    quantity = max(int(request.POST.get("quantity", 1)), 0)
    cart = request.session.get("cart", {})

    if quantity == 0:
        cart.pop(str(pk), None)
    else:
        cart[str(pk)] = min(quantity, product.stock)

    request.session["cart"] = cart
    messages.success(request, "Cart updated.")
    return redirect("cart")


def remove_from_cart(request, pk):
    cart = request.session.get("cart", {})
    cart.pop(str(pk), None)
    request.session["cart"] = cart
    messages.success(request, "Item removed from cart.")
    return redirect("cart")


@login_required
def checkout(request):
    items, total = _cart_data(request)

    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("home")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Re-check stock inside the transaction.
                locked_products = {
                    p.id: p for p in Product.objects.select_for_update().filter(
                        id__in=[item["product"].id for item in items]
                    )
                }

                for item in items:
                    product = locked_products[item["product"].id]
                    if item["quantity"] > product.stock:
                        messages.error(
                            request,
                            f"Not enough stock for {product.name}. Please update your cart.",
                        )
                        return redirect("cart")

                order = Order.objects.create(
                    user=request.user,
                    full_name=form.cleaned_data["full_name"],
                    email=form.cleaned_data["email"],
                    phone=form.cleaned_data["phone"],
                    address=form.cleaned_data["address"],
                    city=form.cleaned_data["city"],
                    pincode=form.cleaned_data["pincode"],
                    total_amount=total,
                )

                for item in items:
                    product = locked_products[item["product"].id]
                    quantity = item["quantity"]
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price,
                    )
                    product.stock -= quantity
                    product.save(update_fields=["stock"])

            request.session["cart"] = {}
            return redirect("order_success", pk=order.pk)
    else:
        form = CheckoutForm(initial={
            "full_name": request.user.get_full_name() or request.user.username,
            "email": request.user.email,
        })

    return render(request, "shop/checkout.html", {
        "form": form,
        "items": items,
        "total": total,
    })


@login_required
def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "shop/order_success.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "shop/my_orders.html", {"orders": orders})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})

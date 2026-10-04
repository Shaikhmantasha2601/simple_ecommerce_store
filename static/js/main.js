document.addEventListener("DOMContentLoaded", () => {
    // Automatically fade Django messages after a few seconds.
    const messages = document.querySelectorAll(".message");
    messages.forEach((message) => {
        setTimeout(() => {
            message.classList.add("hide");
        }, 4000);
    });

    // Prevent accidental checkout/order double-submission.
    document.querySelectorAll("form").forEach((form) => {
        if (form.querySelector('button[type="submit"]')) {
            form.addEventListener("submit", () => {
                const button = form.querySelector('button[type="submit"]');
                if (button && form.closest(".form-card")) {
                    button.disabled = true;
                    button.textContent = "Processing...";
                }
            });
        }
    });
});

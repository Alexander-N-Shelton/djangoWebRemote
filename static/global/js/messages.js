// static/js/messages.js
document.addEventListener('DOMContentLoaded', () => {
    const modals = document.querySelectorAll('[id^="systemMessageModal"]');
    modals.forEach(modalEl => {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    });
});

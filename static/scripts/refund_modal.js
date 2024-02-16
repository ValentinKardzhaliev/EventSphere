document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('refundConfirmationModal');
    const overlay = document.getElementById('overlay');
    const refundForm = document.getElementById('refundForm');
    const confirmationText = document.getElementById('refundConfirmationText');

    const refundButtons = document.querySelectorAll('.refund-button');
    refundButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            const eventId = this.getAttribute('data-event-id');
            const eventName = this.getAttribute('data-event-name');
            const actionUrl = `/tickets/${eventId}/refund/`;
            refundForm.setAttribute('action', actionUrl);

            confirmationText.textContent = `Are you sure you want to refund 1 ticket(s) for ${eventName}?`;

            modal.classList.add('active');
            overlay.classList.add('active');
        });
    });

    window.onclick = function (event) {
        if (event.target === modal) {
            modal.classList.remove('active');
            overlay.classList.remove('active');
        }
    };
});

function closeRefundModal() {
    const modal = document.getElementById('refundConfirmationModal');
    const overlay = document.getElementById('overlay');

    modal.classList.remove('active');
    overlay.classList.remove('active');
}

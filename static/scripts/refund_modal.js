document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('refundConfirmationModal');
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
            modal.style.display = 'block';
        });
    });

    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
});

function closeRefundModal() {
    const modal = document.getElementById('refundConfirmationModal');
    modal.style.display = 'none';
}

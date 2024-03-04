document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('purchaseConfirmationModal');
    const overlay = document.getElementById('purchaseConfirmationOverlay');
    const purchaseForm = document.querySelector('.purchase-form');
    const confirmationText = document.getElementById('purchaseConfirmationText');

    const purchaseButtons = document.querySelectorAll('.purchase-button');
    purchaseButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            const eventId = this.getAttribute('data-event-id');
            const eventName = this.getAttribute('data-event-name');
            const actionUrl = `/tickets/${eventId}/purchase/`;

            const quantityInput = purchaseForm.querySelector('[name="quantity"]');
            console.log('Quantity Input:', quantityInput);

            const quantity = quantityInput?.value;
            console.log('Quantity:', quantity);

            confirmationText.textContent = `Are you sure you want to purchase ${quantity} ticket(s) for ${eventName}?`;

            modal.classList.add('active');
            overlay.classList.add('active');
        });
    });

    window.onclick = function (event) {
        if (event.target === modal) {
            closePurchaseConfirmationModal();
        }
    };
});

function closePurchaseConfirmationModal() {
    const modal = document.getElementById('purchaseConfirmationModal');
    const overlay = document.getElementById('purchaseConfirmationOverlay');

    modal.classList.remove('active');
    overlay.classList.remove('active');
}

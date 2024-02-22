document.addEventListener("DOMContentLoaded", function () {
    var vipTicketsButton = document.getElementById("toggleVipTickets");
    var vipTicketsDiv = document.getElementById("vip-tickets");
    var vipTicketsHeader = document.getElementById("vip-tickets-header");

    // Hide VIP tickets on page load
    vipTicketsDiv.classList.add("hidden");
    vipTicketsHeader.classList.add("hidden");

    function updateVipTicketAttributes() {
        var vipFields = vipTicketsDiv.querySelectorAll('[name="quantity_available"], [name="price_per_ticket"]');
        vipFields.forEach(function (field) {
            field.required = !vipTicketsDiv.classList.contains("hidden");
            if (field.required) {
                field.setAttribute('required', 'required'); // Add the required attribute
            } else {
                field.removeAttribute('required'); // Remove the required attribute
            }
        });
    }

    // Initial update on page load
    updateVipTicketAttributes();

    vipTicketsButton.addEventListener("click", function () {
        vipTicketsDiv.classList.toggle("hidden");
        vipTicketsHeader.classList.toggle("hidden");

        // Update VIP ticket attributes when the button is clicked
        updateVipTicketAttributes();

        vipTicketsButton.textContent = vipTicketsDiv.classList.contains("hidden") ? "Add VIP Tickets" : "Remove VIP Tickets";
    });

});

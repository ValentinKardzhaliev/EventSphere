document.addEventListener('DOMContentLoaded', function () {
    var toggleVipTicketsButton = document.getElementById('toggleVipTickets');

    if (toggleVipTicketsButton) {
        toggleVipTicketsButton.addEventListener('click', function () {
            var vipTicketsHeader = document.getElementById('vip-tickets-header');
            var vipTicketForm = document.getElementById('vipTicketForm');

            if (vipTicketsHeader && vipTicketForm) {
                if (vipTicketsHeader.style.display === 'none') {
                    vipTicketsHeader.style.display = 'block';
                    vipTicketForm.style.display = 'block';
                } else {
                    vipTicketsHeader.style.display = 'none';
                    vipTicketForm.style.display = 'none';
                }
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('addVipButton').addEventListener('click', function () {
        document.getElementById('vipTicketForm').style.display = 'block';
        document.getElementById('vip-tickets-header').style.display = 'block';
    });

    document.getElementById('saveEventButton').addEventListener('click', function () {
        document.getElementById('eventAndTicketsForm').submit();
    });
});

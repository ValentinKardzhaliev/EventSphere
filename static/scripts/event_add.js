document.addEventListener("DOMContentLoaded", function () {
    var vipTicketsButton = document.getElementById("toggleVipTickets");
    var vipTicketsDiv = document.getElementById("vip-tickets");
    var vipTicketsHeader = document.getElementById("vip-tickets-header");

    vipTicketsButton.addEventListener("click", function () {
        if (vipTicketsDiv.style.display === "none") {
            vipTicketsDiv.style.display = "block";
            vipTicketsHeader.style.display = "block";
            vipTicketsButton.textContent = "Remove VIP Tickets";
        } else {
            vipTicketsDiv.style.display = "none";
            vipTicketsHeader.style.display = "none";
            vipTicketsButton.textContent = "Add VIP Tickets";
        }
    });
});

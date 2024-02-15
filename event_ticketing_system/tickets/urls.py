from django.urls import path
from .views import TicketPurchaseView, TicketPurchaseSuccessView, TicketPurchaseFailureView, UserTicketsView, \
    RefundTicketView

urlpatterns = [
    path('<int:pk>/purchase/', TicketPurchaseView.as_view(), name='ticket_purchase'),
    path('purchase/success/<int:pk>/', TicketPurchaseSuccessView.as_view(), name='ticket_purchase_success'),
    path('purchase/failure/', TicketPurchaseFailureView.as_view(), name='ticket_purchase_failure'),
    path('user-tickets/<int:pk>/', UserTicketsView.as_view(), name='user_tickets'),
    path('<int:event_id>/refund/', RefundTicketView.as_view(), name='refund_ticket'),
]

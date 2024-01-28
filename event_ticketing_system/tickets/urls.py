from django.urls import path
from .views import TicketPurchaseView, TicketPurchaseSuccessView, TicketPurchaseFailureView

urlpatterns = [
    path('<int:pk>/purchase/', TicketPurchaseView.as_view(), name='ticket_purchase'),
    path('purchase/success/<int:pk>/', TicketPurchaseSuccessView.as_view(), name='ticket_purchase_success'),
    path('purchase/failure/', TicketPurchaseFailureView.as_view(), name='ticket_purchase_failure'),
]

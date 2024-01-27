from django.urls import path

from event_ticketing_system.events.views import EventAddView, EventDetailsView, user_created_events, \
    PurchaseSuccessView, PurchaseFailureView

urlpatterns = [
    path('add/', EventAddView.as_view(), name='event add'),
    path('<int:pk>/', EventDetailsView.as_view(), name='event_details'),
    path('user-events/', user_created_events, name='user_created_events'),
    path('event/<int:pk>/purchase/', EventDetailsView.as_view(), name='event_purchase'),
    path('purchase/success/<int:pk>/', PurchaseSuccessView.as_view(), name='purchase_success'),
    path('purchase/failure/', PurchaseFailureView.as_view(), name='purchase_failure'),
]

from django.urls import path
from .views import (
    EventAddView,
    EventDetailsView,
    user_created_events,
)

urlpatterns = [
    path('add/', EventAddView.as_view(), name='event_add'),
    path('<int:pk>/', EventDetailsView.as_view(), name='event_details'),
    path('user-events/', user_created_events, name='user_created_events'),
]

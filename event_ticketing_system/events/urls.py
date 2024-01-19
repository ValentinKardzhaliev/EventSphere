from django.urls import path

from event_ticketing_system.events.views import EventAddView, EventDetailsView, user_created_events

urlpatterns = [
    path('add/', EventAddView.as_view(), name='event add'),
    path('<int:pk>/', EventDetailsView.as_view(), name='event details'),
    path('user-events/', user_created_events, name='user_created_events')
]

from django.urls import path

from event_ticketing_system.events.views import EventAddView, EventDetailsView

urlpatterns = [
    path('add/', EventAddView.as_view(), name='event add'),
    path('<int:pk>/', EventDetailsView.as_view(), name='event detail'),
]

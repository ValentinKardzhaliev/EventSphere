from django.urls import path

from event_ticketing_system.events.views import EventAddView, EventDetailsView, EventDeleteView

urlpatterns = [
    path('add/', EventAddView.as_view(), name='event add'),
    path('<int:pk>/', EventDetailsView.as_view(), name='event detail'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
]

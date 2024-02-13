from django.template.defaulttags import url
from django.urls import path
from .views import (
    EventAddView,
    EventDetailsView,
    user_created_events, events_by_category, LocationAutocomplete, EventEditView,
)

urlpatterns = [
    path('add/', EventAddView.as_view(), name='event_add'),
    path('<int:pk>/', EventDetailsView.as_view(), name='event_details'),
    path('user-events/', user_created_events, name='user_created_events'),
    path('category/<str:category>/', events_by_category, name='events_by_category'),
    path('location-autocomplete/', LocationAutocomplete.as_view(), name='location-autocomplete'),
    path('edit/<int:pk>/', EventEditView.as_view(), name='event_edit'),
]



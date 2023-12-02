from django.urls import path
from .views import index, like_event, liked_events_view

urlpatterns = [
    path('', index, name='index'),
    path('like_event/<int:event_id>/', like_event, name='like_event'),
    path('liked_events/', liked_events_view, name='liked_events')
]

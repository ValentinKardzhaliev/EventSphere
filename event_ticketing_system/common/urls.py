from django.urls import path
from .views import like_functionality, index

urlpatterns = [
    path('', index, name='index'),
    path('like/<int:event_id>/', like_functionality, name='like_event'),
]

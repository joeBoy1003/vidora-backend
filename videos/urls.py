from django.urls import path
from .views import VideoAPIView

urlpatterns = [
    path('upload', VideoAPIView.as_view(), name='video-upload'),
    path('getAll', VideoAPIView.as_view(), name='video-list'),
    path('<int:pk>/delete', VideoAPIView.as_view(), name='video-delete'),
]

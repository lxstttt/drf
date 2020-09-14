
from django.urls import path

from app1 import views

urlpatterns = [
    path("users/", views.UserAPIView.as_view()),
    path("users/<str:id>/", views.UserAPIView.as_view()),
]
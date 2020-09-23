from django.urls import path

from app2 import views

urlpatterns = [
    path('trees/',views.TreeAPIView.as_view()),
    path('trees/<str:id>/',views.TreeAPIView.as_view()),
]
from django.urls import path

from app1 import views

urlpatterns = [
    path('book/',views.BookAPIView.as_view()),
    path('book2/',views.BookAPIView2.as_view()),
    path('book/<str:id>/',views.BookAPIView.as_view()),
    path('book2/<str:id>/',views.BookAPIView2.as_view()),
]
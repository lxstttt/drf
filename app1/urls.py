
from django.urls import path

from app1 import views

urlpatterns = [
    path('hello/',views.hello),
    path('user/',views.UserView.as_view()),
    path('djl/<str:id>/',views.Djl.as_view()),
    path('djl/',views.Djl.as_view()),
    path('user2/<str:id>/',views.UserAPI.as_view()),
    path('user2/',views.UserAPI.as_view()),
]
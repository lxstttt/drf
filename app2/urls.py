from django.urls import path

from app2 import views

urlpatterns = [
    path('student/',views.StudentAPIView.as_view()),
    path('student/<str:id>/',views.StudentAPIView.as_view()),

    path("generic/", views.StudentGenericAPIView.as_view()),
    path("generic/<str:id>/", views.StudentGenericAPIView.as_view()),

    path("mixin/", views.StudentGenericMixinView.as_view()),
    path("mixin/<str:id>/", views.StudentGenericMixinView.as_view()),

    path("viewset/", views.StudentModelViewSet.as_view({"post": "user_login", "get": "user_register"})),
    path("viewset/<str:id>/", views.StudentModelViewSet.as_view({"post": "user_login", "get": "user_register"})),

]
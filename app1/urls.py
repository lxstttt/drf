"""drf_ems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from app1 import views
from drf_ems2 import settings

urlpatterns = [
    path('users/',views.UserAPIView.as_view()),
    path('users/<str:id>/',views.UserAPIView.as_view()),

    path('employee/',views.EmployeeGenericAPIView.as_view()),
    path('employee/<str:id>/',views.EmployeeGenericAPIView.as_view()),

    path('login/',views.LoginAPIView.as_view()),
    path('login/<str:id>/',views.LoginAPIView.as_view()),

    path('update/',views.EmpUpdateAPIView.as_view()),
    path('update/<str:id>/',views.EmpUpdateAPIView.as_view()),
]

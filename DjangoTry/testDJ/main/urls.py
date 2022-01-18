"""testDJ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from . import views
from .views import *

urlpatterns = [
    path("", views.main, name="main"),
    path("catalogue", views.catalog, name="catalog"),
    path('instruction', views.instruction, name="instruction"),
    path("form", views.formBook, name="formBook"),
    path('bookInfo/<int:id>/',views.bookInfo,name="bookInfo"),


    path('test1', views.gen, name='g'),
    path('test2', views.scan, name='s'),
    path('test3', views.delete, name='del'),




    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
]

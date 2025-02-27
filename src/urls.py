"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from .views import BaseView, HomePartialView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), # Allauth
    path("__reload__/", include("django_browser_reload.urls")),
    #path('accounts/login/', include('allauth.urls'), name='login'), # Allauth
    #path('', include('apps.app.urls')),
    path('', BaseView.as_view(), name='base'),
    path('home/', HomePartialView.as_view(), name='home_partial'),
    path('menu1/', include('apps.menu1.urls')),
    path('menu2/', include('apps.menu2.urls')),
    path('login/', include('apps.loginapp.urls')),
]

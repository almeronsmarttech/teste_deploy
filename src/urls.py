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
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import BaseView, HomePartialView

from apps.loginapp.views import header_partial, FormPartialView, UserCreationView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), # Allauth
    path("__reload__/", include("django_browser_reload.urls")),
    #path('accounts/login/', include('allauth.urls'), name='login'), # Allauth
    #path('', include('apps.app.urls')),
    path('', BaseView.as_view(), name='base'),
    path('home/', HomePartialView.as_view(), name='home_partial'),
    path('laje/', include('apps.laje_metodo_araujo.urls')),
    path('menu2/', include('apps.menu2.urls')),
    path('login/', include('apps.loginapp.urls')),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('header/', header_partial, name='header_partial'),
    path('form/', FormPartialView.as_view(), name='form_partial'),
    path('create-account/', UserCreationView.as_view(), name='create_account'),
    path('subscriptions/', include('apps.subscriptions.urls', namespace='subscriptions')),
]

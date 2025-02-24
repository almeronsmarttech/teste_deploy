from django.urls import path
from .views import FormPartialView

app_name = 'loginapp'

urlpatterns = [
    path('form/', FormPartialView.as_view(), name='form_partial'),
]

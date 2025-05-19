# apps/subscriptions/urls.py

from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),
    # (opcional no futuro) path('webhook/', views.webhook, name='webhook'),
    path('test-payment-methods/', views.test_payment_methods, name='test_payment_methods'),
path('process-payment/', views.process_payment, name='process_payment'),
]

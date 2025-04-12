from django.urls import path
#from django.contrib.auth.views import LogoutView
from .views import (FormPartialView, EmailLoginView, VerifyCodeView, ResendCodeView, SendVerificationCodeView,
                    SignupPartialView, header_partial)
    #CustomLogoutView,
    #                get_csrf_token)
from apps.loginapp.views import UserCreationView
app_name = 'loginapp'

urlpatterns = [
    path('form/', FormPartialView.as_view(), name='form_partial'),
    path("login/", EmailLoginView.as_view(), name="send_code"),
    #path("logout/", CustomLogoutView.as_view(), name="logout"),
    #path("accounts/logout/", LogoutView.as_view(), name="logout"),
    #path("accounts/logout/", LogoutView.as_view(next_page="/"), name="logout"),
    #path("logout/", CustomLogoutView.as_view(), name="logout"),
    #path('logout/', LogoutView.as_view(), name='logout'),
    #path("api/csrf-token/", get_csrf_token, name="get-csrf-token"),
    path("verify_code/", VerifyCodeView.as_view(), name="verify_code"),
    path("resend_code/", ResendCodeView.as_view(), name="resend_code"),
    path("send_code/", EmailLoginView.as_view(), name="send_code"),
    path("send_verification_code/", SendVerificationCodeView.as_view(), name="send_verification_code"),
    path("signup/", SignupPartialView.as_view(), name="signup_partial"),
    path("send_verification_code/", SendVerificationCodeView.as_view(), name="send_verification_code"),
    path("verify_code/", VerifyCodeView.as_view(), name="verify_code"),
    #path("header/", header_partial, name="header_partial"),
    path('criar-conta/', UserCreationView.as_view(), name='user_creation_form'),
]

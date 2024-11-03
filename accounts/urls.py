from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('verify-otp/', views.verify_otp, name='verify_otp'),  # OTP for registration
    path('verify-login-otp/', views.verify_login_otp, name='verify_login_otp'),  # OTP for login
    path('resend-otp/', views.resend_otp,  name='resend_otp'),  # Resend OTP
    path('change_profile_photo/', views.change_profile_photo, name="change_profile_photo"),
    path('update_profile_info/', views.update_profile_info, name="update_profile_info")
]

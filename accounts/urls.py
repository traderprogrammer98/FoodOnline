from django.urls import path

from accounts import views

urlpatterns = [
    path("register-user", views.register_user, name="register_user", ),
    path("register-vendor", views.register_vendor, name="register_vendor", ),
    path("login", views.login, name="login", ),
    path("logout", views.logout, name="logout", ),
    path("customer-dashboard", views.customer_dashboard, name="customer_dashboard", ),
    path("vendor-dashboard", views.vendor_dashboard, name="vendor_dashboard", ),
    path("verify-email/<uidb64>/<token>", views.verify_email, name="verify_email", ),
    path("forgot-password", views.forgot_password, name="forgot_password", ),
    path("reset-password", views.reset_password, name="reset_password", ),
    path("reset-password-validate/<uidb64>/<token>", views.reset_password_validate, name="reset_password_validate", ),
]

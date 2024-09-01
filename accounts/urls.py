from django.urls import path

from accounts import views

urlpatterns = [
    path("register-user", views.register_user, name="register_user", )
]
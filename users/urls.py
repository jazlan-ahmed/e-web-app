from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.user_registration, name="register"),
    path("verify/", views.verify_registration_code, name="verify"),
    path("resend-code/", views.resend_verification_code, name="resend-code"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("address/add/", views.add_address, name="add_address"),
    path("ajax/load-states/", views.load_states, name="ajax_load_states"),
    path("ajax/load-cities/", views.load_cities, name="ajax_load_cities"),
]

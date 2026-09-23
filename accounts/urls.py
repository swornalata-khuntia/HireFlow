from django.urls import path

from .views import (
    signup_view,
    login_view,
    logout_view,
    candidate_profile_view,
    settings_view,
)


urlpatterns = [

    path(
        "signup/",
        signup_view,
        name="signup"
    ),

    path(
        "login/",
        login_view,
        name="login"
    ),

    path(
        "logout/",
        logout_view,
        name="logout"
    ),

    path(
        "profile/",
        candidate_profile_view,
        name="candidate_profile"
    ),
    path(
        "settings/",
        settings_view,
        name="account_settings"
    ),

]
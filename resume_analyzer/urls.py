from django.urls import path
from .views import resume_upload


urlpatterns = [
    path("", resume_upload, name="resume_upload"),
]
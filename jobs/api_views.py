from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Job
from .api_serializers import JobSerializer


class JobListAPIView(generics.ListAPIView):

    queryset = Job.objects.all().order_by("-created_at")

    serializer_class = JobSerializer

    permission_classes = [
        AllowAny
    ]


class JobDetailAPIView(generics.RetrieveAPIView):

    queryset = Job.objects.all()

    serializer_class = JobSerializer

    permission_classes = [
        AllowAny
    ]


class JobCreateAPIView(generics.CreateAPIView):

    serializer_class = JobSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(self, serializer):

        profile = self.request.user.profile

        if profile.role != "recruiter":

            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "Only recruiters can create jobs."
            )

        serializer.save(
            company=profile.company_name
        )
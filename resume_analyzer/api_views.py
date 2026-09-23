from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Resume
from .api_serializers import ResumeSerializer


class MyResumeAPIView(generics.ListAPIView):

    serializer_class = ResumeSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Resume.objects.filter(
            user=self.request.user
        ).order_by(
            "-uploaded_at"
        )
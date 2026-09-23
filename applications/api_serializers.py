from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):

    candidate = serializers.CharField(
        source="user.username",
        read_only=True
    )

    job_title = serializers.CharField(
        source="job.title",
        read_only=True
    )

    company = serializers.CharField(
        source="job.company",
        read_only=True
    )

    class Meta:

        model = Application

        fields = [
            "id",
            "candidate",
            "job_title",
            "company",
            "status",
            "applied_at",
        ]

        read_only_fields = [
            "id",
            "candidate",
            "job_title",
            "company",
            "applied_at",
        ]
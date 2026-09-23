from rest_framework import serializers

from .models import Job


class JobSerializer(serializers.ModelSerializer):

    class Meta:

        model = Job

        fields = [
            "id",
            "title",
            "company",
            "location",
            "required_skills",
            "salary",
            "job_type",
            "description",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "company",
            "created_at",
        ]
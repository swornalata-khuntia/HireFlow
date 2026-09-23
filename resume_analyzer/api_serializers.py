from rest_framework import serializers

from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:

        model = Resume

        fields = [
            "id",
            "username",
            "resume_file",
            "extracted_text",
            "uploaded_at",
        ]

        read_only_fields = [
            "id",
            "username",
            "extracted_text",
            "uploaded_at",
        ]
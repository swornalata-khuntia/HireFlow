from django.db import models


class Job(models.Model):

    title = models.CharField(max_length=200)

    company = models.CharField(max_length=200)

    location = models.CharField(max_length=200)

    required_skills = models.TextField(
        help_text="Enter skills separated by commas"
    )

    salary = models.CharField(
        max_length=100,
        blank=True
    )

    job_type = models.CharField(
        max_length=100,
        default="Full Time"
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.title} - {self.company}"
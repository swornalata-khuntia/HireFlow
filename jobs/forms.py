from django import forms
from .models import Job


class JobForm(forms.ModelForm):

    class Meta:
        model = Job

        fields = [
            "title",
            "location",
            "required_skills",
            "salary",
            "job_type",
            "description",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Python Django Developer"
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Bhubaneswar"
                }
            ),

            "required_skills": forms.TextInput(
                attrs={
                    "placeholder": "Python, Django, MySQL, REST API, Git"
                }
            ),

            "salary": forms.TextInput(
                attrs={
                    "placeholder": "e.g. 3 - 5 LPA"
                }
            ),

            "job_type": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Full Time"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Write the job description...",
                    "rows": 6
                }
            ),
        }
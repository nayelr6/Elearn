from django.forms import ModelForm
from .models import Exam

class CreateExamForm(ModelForm):
    class Meta:
        model = Exam
        fields = ["Exam_date"]
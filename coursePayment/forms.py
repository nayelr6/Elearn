from django import forms
from .models import CoursePayment

class Withdrawal(forms.ModelForm):
    class Meta:
        model = CoursePayment
        fields = []

from django.db import models
from exam.models import Exam
# Create your models here.

class Question(models.Model):
    exam=models.ForeignKey(Exam, on_delete=models.CASCADE)
    qs = models.CharField(max_length=200)
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100)
    option_4 = models.CharField(max_length=100)
    correct = models.CharField(max_length=100)
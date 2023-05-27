from django.db import models

# Create your models here.
from course.models import Course

class Exam(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    Exam_date=models.DateField()
from django.db import models
from users.models import Student
from exam.models import Exam

class takes_exam(models.Model):
    student= models.ForeignKey(Student, on_delete=models.CASCADE)
    exam =models.ForeignKey(Exam, on_delete=models.CASCADE)
    feedback=models.TextField()
    marks=models.DecimalField(max_digits=5, decimal_places=2)
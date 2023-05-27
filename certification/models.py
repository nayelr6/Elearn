from django.db import models
from users.models import Teacher

class Certification(models.Model):
    teacher_id= models.ForeignKey(Teacher, on_delete=models.CASCADE)
    certificates= models.CharField(max_length= 50)


# Create your models here.

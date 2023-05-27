from django.db import models
from users.models import Teacher

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    timeline = models.CharField(max_length=50)
    owner = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    fees = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    # def __str__(self):
    #     return self.title
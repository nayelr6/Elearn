from django.db import models
from users.models import Student
from course.models import Course
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Review(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[
                                 MinValueValidator(0), MaxValueValidator(5)])
    comment = models.CharField(max_length=100)

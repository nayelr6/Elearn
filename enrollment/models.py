from django.db import models
from users.models import Student
from course.models import Course
# Create your models here.

class Enrollment(models.Model):
    student_id= models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id= models.ForeignKey(Course, on_delete= models.CASCADE)
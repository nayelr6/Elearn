from django.db import models
from users.models import Student, Teacher
from course.models import Course
# Create your models here.

class CoursePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
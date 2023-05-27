from django.db import models
from users.models import User
from course.models import Course

class Forum(models.Model):
    course_id= models.ForeignKey(Course, on_delete=models.CASCADE)

class Message(models.Model):
    forum_id = models.ForeignKey(Forum, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    # date_posted = models.DateTimeField(auto_now_add=True)
    msg = models.TextField()

# Create your models here.

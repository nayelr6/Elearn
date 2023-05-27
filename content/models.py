from django.db import models
from course.models import Course

# Create your models here.
class Content(models.Model):
    video = models.FileField(upload_to='videos/')
    content_title = models.CharField(max_length=150)
    notes = models.TextField()
    c_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.content_title
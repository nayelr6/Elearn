from django.dispatch import receiver
from course.models import Course
from django.db.models.signals import post_save
from .models import Forum

@receiver(post_save, sender=Course)
def create_forum(sender, instance, created, **kwargs):
    if created:
        Forum.objects.create(course_id=instance)
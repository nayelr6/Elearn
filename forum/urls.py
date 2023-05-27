from django.urls import path
from .views import view_forum

urlpatterns = [
    path("", view_forum, name='course-forum'),
]
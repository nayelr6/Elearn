from django.urls import path, include
from .views import ExamListView, ExamDetailView, create_exam, DeleteExamView

urlpatterns = [
    path("", ExamListView.as_view(), name="exam-list"),
    path("<int:exam_id>/", ExamDetailView.as_view(), name="exam-detail"),
    path("new/", create_exam, name="create-exam"),
    path("<int:exam_id>/delete/", DeleteExamView.as_view(), name="delete-exam"),
    path("<int:exam_id>/questions/", include("questions.urls")),
]
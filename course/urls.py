from django.urls import path, include
from .views import CourseListView, CourseCreateView, CourseUpdateView, CourseDetailView, CourseDeleteView, owned_courses, OwnedCourseDetailView
from content.views import ownedContentListView, OwnedContentDetailView, ContentUpdateView, ContentDeleteView, ContentCreateView
from enrollment.views import CreateEnrollmentView
from coursePayment.views import StudentExamListView, StudentExamDetailView, st_exam_questions, st_exam, save_quiz_view, exam_result, payment_update_view
from exam.views import examListView, ExamDetailView, create_exam, DeleteExamView
from questions.views import questionListView, QuestionCreateView, QuestionDetailView, QuestionDeleteView, QuestionUpdateView
from reviews.views import ReviewListView

urlpatterns = [
    path('', CourseListView.as_view(), name="course-home"),
    path('course/<int:pk>/', CourseDetailView.as_view(), name="course-detail"),
    path('owned/new/', CourseCreateView.as_view(), name="course-create"),
    path('owned/<int:pk>/update/', CourseUpdateView.as_view(), name="course-update"),
    path('owned/<int:pk>/delete/', CourseDeleteView.as_view(), name="course-delete"),
    path('course/<int:course_pk>/', include('content.urls')),
    path('course/<int:pk>/enroll/', CreateEnrollmentView.as_view(), name="course-enroll"),
    path("course/<int:pk>/forum/", include('forum.urls')),
    path('course/<int:pk>/exam/', include("exam.urls")),
    path('course/<int:course_pk>/st_exam/', StudentExamListView.as_view(), name="st-exam"),
    path('course/<int:course_pk>/st_exam/<int:pk>/', StudentExamDetailView.as_view(), name="st-exam-detail"),
    path('course/<int:course_pk>/st_exam/<int:pk>/st_question_list/questions/', st_exam_questions, name="st-exam-questions"),
    path('course/<int:course_pk>/st_exam/<int:pk>/st_question_list/', st_exam, name="st-exam"),
    path('course/<int:course_pk>/st_exam/<int:pk>/st_question_list/save/', save_quiz_view, name="st-exam-save"),
    path('course/<int:course_pk>/st_exam/<int:pk>/results/', exam_result, name="exam-result"),
    path('owned/', owned_courses, name='owned-courses'),
    path('owned/<int:pk>/', OwnedCourseDetailView.as_view(), name="owned-course-detail"),
    path('owned/<int:course_pk>/withdraw/', payment_update_view, name="withdraw"),
    path('owned/<int:course_pk>/content/', ownedContentListView, name="owned-content-list"),
    path('owned/<int:course_pk>/content/<int:pk>/', OwnedContentDetailView.as_view(), name="owned-content-detail"),
    path('owned/<int:course_pk>/content/update/<int:pk>/', ContentUpdateView.as_view(), name="content-update"),
    path('owned/<int:course_pk>/content/new/', ContentCreateView.as_view(), name="content-create"),
    path('owned/<int:course_pk>/content/delete/<int:pk>/', ContentDeleteView.as_view(), name="content-delete"),
    path('owned/<int:pk>/exams/', examListView, name="exam-list"),
    path('owned/<int:course_pk>/exams/<int:pk>/', ExamDetailView.as_view(), name="exam-detail"),
    path('owned/<int:course_pk>/exams/new/', create_exam, name="exam-create"),
    path('owned/<int:course_pk>/exams/<int:pk>/delete/', DeleteExamView.as_view(), name="delete-exam"), 
    path('owned/<int:course_pk>/exams/<int:exam_id>/questions/', questionListView, name="exam-question-list"),
    path('owned/<int:course_pk>/exams/<int:exam_id>/questions/new/', QuestionCreateView.as_view(), name="exam-question-create"),
    path('owned/<int:course_pk>/exams/<int:exam_id>/questions/<int:pk>/', QuestionDetailView.as_view(), name="exam-question-detail"), 
    path('owned/<int:course_pk>/exams/<int:exam_id>/questions/<int:pk>/update/', QuestionUpdateView.as_view(), name="exam-question-update"), 
    path('owned/<int:course_pk>/exams/<int:exam_id>/questions/<int:pk>/delete/', QuestionDeleteView.as_view(), name="exam-question-delete"), 
    path('course/<int:pk>/reviews/', ReviewListView.as_view(), name="review-list"),
]
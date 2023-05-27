from django.urls import path
from .views import EnrollCourseView, UnenrollCourse, EnrollCourseDetailView
from coursePayment.views import PaymentCreateView
from reviews.views import ReviewDetailView, add_review, ReviewDeleteView, update_review

urlpatterns = [
    path("", EnrollCourseView.as_view(), name="enrolled-courses"),
    path("<int:pk>/", EnrollCourseDetailView.as_view(), name="enrolled-course-detail"),
    path("<int:pk>/delete/", UnenrollCourse.as_view(), name="unenroll-course"),
    path("<int:pk>/purchase/", PaymentCreateView.as_view(), name="purchase-course"),
    path('<int:enr_pk>/review/<int:pk>/', ReviewDetailView.as_view(), name="review-detail"),
    path('<int:enr_pk>/reviews/create/', add_review, name="review-create"),
    path('<int:course_id>/review/<int:pk>/delete/', ReviewDeleteView.as_view(), name="review-delete"),
    path('<int:course_id>/review/<int:pk>/update/', update_review, name="review-update"),
]
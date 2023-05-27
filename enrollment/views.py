from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from .models import Enrollment
from users.models import Student
from course.models import Course
from coursePayment.models import CoursePayment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

class CreateEnrollmentView(LoginRequiredMixin, CreateView):
    model = Enrollment
    fields = []
    success_url = "/"

    def form_valid(self, form):
        form.instance.student_id = Student.objects.filter(user=self.request.user).first()
        form.instance.course_id = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        return super().form_valid(form)
    
class EnrollCourseView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = "enrollment/enrolled_courses.html"
    context_object_name = "enrolled_courses"

    def get_queryset(self):
        st_id = Student.objects.filter(user=self.request.user).first()
        payments = CoursePayment.objects.filter(student=st_id)

        purchased_courses = []
        for payment in payments:
            purchased_courses.append(payment.course)

        return Enrollment.objects.filter(student_id=st_id).exclude(course_id__in =purchased_courses)
    
class EnrollCourseDetailView(LoginRequiredMixin, DetailView):
    model = Enrollment
    template_name = "enrollment/enrolled_course_detail.html"

class UnenrollCourse(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Enrollment
    success_url = "/enrolled/"

    def test_func(self):
        enroll = self.get_object()
        if self.request.user == enroll.student_id.user:
            return True
        return False      

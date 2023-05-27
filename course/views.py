from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import Teacher, Student
from enrollment.models import Enrollment
from reviews.models import Review
# Create your views here.

class CourseListView(ListView):
    model = Course
    template_name="course/course_list.html"
    context_object_name = "courses"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            student_id = get_object_or_404(Student, user=self.request.user)
            enrolled_courses = Enrollment.objects.filter(student_id=student_id)
            teacher_id = get_object_or_404(Teacher, user=self.request.user)

            enrollment_list = []
            for enrolled_course in enrolled_courses:
                enrollment_list.append(enrolled_course.course_id.id)

            chosen_courses = Course.objects.all().exclude(id__in = enrollment_list).exclude(owner = teacher_id)

            for course in chosen_courses:
                reviews_list = Review.objects.filter(course_id=course)
                avg_rating = 0
                for review in reviews_list:
                    avg_rating += review.rating
                if len(reviews_list) == 0:
                    avg_rating = 0
                else:
                    avg_rating = avg_rating/len(reviews_list)

                avg_rating = float(avg_rating)
                course.avg_rating = round(avg_rating, 1)


            return chosen_courses
        else:
            chosen_courses = Course.objects.all()

            for course in chosen_courses:
                reviews_list = Review.objects.filter(course_id=course)
                avg_rating = 0
                for review in reviews_list:
                    avg_rating += review.rating
                if len(reviews_list) == 0:
                    avg_rating = 0
                else:
                    avg_rating = avg_rating/len(reviews_list)

                course.avg_rating = avg_rating

            return chosen_courses


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name="course/course_detail.html"


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    fields = ["title", "fees", "description", "timeline"]
    success_url = "/"

    def form_valid(self, form):
        form.instance.owner = Teacher.objects.filter(user=self.request.user).first()
        return super().form_valid(form)
    
class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    fields = ["title", "description", "timeline", "fees"]
    success_url = "/"

    def form_valid(self, form):
        form.instance.owner = Teacher.objects.filter(user=self.request.user).first()
        return super().form_valid(form)

    def test_func(self):
        course = self.get_object()
        if self.request.user == course.owner.user:
            return True
        return False
    
class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    success_url = "/"

    def test_func(self):
        course = self.get_object()
        if self.request.user == course.owner.user:
            return True
        return False        
    
def owned_courses(request):
    owner = Teacher.objects.filter(user=request.user).first()
    courses = Course.objects.filter(owner=owner)

    data = {}
    data["courses"] = courses

    return render(request, "course/owned_courses_list.html", data)

class OwnedCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name="course/owned_course_detail.html"

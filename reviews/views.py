from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Review
from .forms import ReviewForm
from users.models import Student
from course.models import Course
from enrollment.models import Enrollment

# Create your views here.
class ReviewListView(ListView):
    model = Review
    template_name="reviews/review_list.html"
    context_object_name = "reviews"

    def get_queryset(self):
        course_id = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        # content = self.get_object()
        return Review.objects.filter(course_id=course_id)

class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    template_name="reviews/review_detail.html"


def add_review(request, enr_pk):
    if(request.method == "POST"):
        form = ReviewForm(request.POST)
        if form.is_valid():
            student_id = get_object_or_404(Student, user=request.user)     
            enrolled_course_id = get_object_or_404(Enrollment, pk=enr_pk)
            course_id = get_object_or_404(Course, pk=enrolled_course_id.course_id.pk)
            form.instance.student_id = student_id
            form.instance.course_id = course_id
            form.save()
            return redirect('enrolled-course-detail', enr_pk)
    else:
        form = ReviewForm()
        enrolled_course_id = get_object_or_404(Enrollment, pk=enr_pk)
        course_id = enrolled_course_id.course_id
        review_list = Review.objects.filter(course_id=course_id)
        review_exists = False
        chosen_review = None
        student_id = get_object_or_404(Student, user=request.user)
        for review in review_list:
            if review.student_id == student_id:
                review_exists = True
                chosen_review = review

        if review_exists==True:
            return redirect('review-detail', enr_pk, chosen_review.pk)
        return render(request, "reviews/create_review.html", {"form" : form, "course": course_id})
    
def update_review(request, course_id, pk):
    chosen_review = get_object_or_404(Review, pk=pk)
    if(request.method == "POST"):
        form = ReviewForm(request.POST, instance=chosen_review)
        if form.is_valid():
            student_id = get_object_or_404(Student, user=request.user)     
            selected_course = get_object_or_404(Course, pk=course_id)
            enrolled_course_id = get_object_or_404(Enrollment, course_id=selected_course)
            form.instance.student_id = student_id
            form.instance.course_id = selected_course
            form.save()
            return redirect('enrolled-course-detail', enrolled_course_id.pk)
    else:
        student_id = get_object_or_404(Student, user=request.user)     
        selected_course = get_object_or_404(Course, pk=course_id)
        enrolled_course_id = get_object_or_404(Enrollment, course_id=selected_course)

        review_list = Review.objects.filter(course_id=selected_course)
        chosen_review = None
        student_id = get_object_or_404(Student, user=request.user)
        for review in review_list:
            if review.student_id == student_id:
                chosen_review = review

        form = ReviewForm(instance=chosen_review)
        return render(request, "reviews/create_review.html", {"form" : form, "course": course_id})

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_url = "/enrolled/"

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.student_id.user:
            return True
        return False     
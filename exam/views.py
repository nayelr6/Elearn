from django.shortcuts import render, get_object_or_404, redirect
from .models import Exam
from django.views.generic import DetailView, ListView, DeleteView
from course.models import Course
from .forms import CreateExamForm
from users.models import Teacher
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = "exam/exam_list.html"
    context_object_name = "exams"

    def get_queryset(self):
        course_id = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        return Exam.objects.filter(course=course_id)

def examListView(request, pk):
    course_id = get_object_or_404(Course, pk=pk)
    exams = Exam.objects.filter(course=course_id)
    exam_data = {}
    exam_data["exams"] = exams
    exam_data["pk"] = pk

    return render(request, "exam/exam_list.html", exam_data)

class ExamDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = "exam/exam_detail.html"
    context_object_name = "exam"

def create_exam(request, course_pk):
    teacher = Teacher.objects.filter(user=request.user).first()
    if request.user.id == teacher.user.id:
        if request.method == "POST":
            form = CreateExamForm(request.POST)
            if form.is_valid():
                form.instance.course=get_object_or_404(Course, pk=course_pk)
                form.save()
                return redirect("course-home")
        else:
            form = CreateExamForm
            return render(request, "exam/exam_create.html", {"form": form})
            
    return render(request, "exam/exam_create.html", {"u_id": request.user.id, "t_id": teacher.user.id})
            
class DeleteExamView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Exam
    success_url = "/owned/"

    def test_func(self):
        exam = self.get_object()
        if self.request.user == exam.course.owner.user:
            return True
        return False        

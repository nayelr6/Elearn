from django.shortcuts import render, get_object_or_404
from .models import Question
from exam.models import Exam
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
# Create your views here.
    
def questionListView(request, course_pk, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        questions = Question.objects.filter(exam=exam)
        data = {}
        data["questions"] = questions
        data["exam"] = exam

        return render(request, "questions/question_list.html", data)

class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name="questions/question_detail.html"


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ["qs", "option_1", "option_2", "option_3", "option_4", "correct"]
    success_url = "/owned/"

    def form_valid(self, form):
        form.instance.exam = Exam.objects.filter(pk=self.kwargs.get('exam_id')).first()
        return super().form_valid(form)
    
class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    fields = ["qs", "option_1", "option_2", "option_3", "option_4", "correct"]
    success_url = "/owned/"  

    def form_valid(self, form):
        form.instance.exam = Exam.objects.filter(pk=self.kwargs.get('exam_id')).first()
        return super().form_valid(form)

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.exam.course.owner.user:
            return True
        return False
    
class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = "/owned/"

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.exam.course.owner.user:
            return True
        return False
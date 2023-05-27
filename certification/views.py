from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Certification
from users.models import Teacher
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

class CertificationListView(ListView):
    model = Certification
    template_name = "certification/certification_list.html"
    context_object_name = "certifications"

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        certifcates = Certification.objects.filter(teacher_id=teacher)
        return certifcates

class CertificationDetailView(LoginRequiredMixin, DetailView):
    model = Certification
    template_name="certification/certification_detail.html"


class CertificationCreateView(LoginRequiredMixin, CreateView):
    model = Certification
    fields = ["certificates"]
    success_url = "/certifications/"

    def form_valid(self, form):
        form.instance.teacher_id = Teacher.objects.filter(user=self.request.user).first()
        return super().form_valid(form)
    
class CertificationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Certification
    fields = ["certificates"]
    success_url = "/certifications/"

    def form_valid(self, form):
        form.instance.teacher_id = Teacher.objects.filter(user=self.request.user).first()
        return super().form_valid(form)

    def test_func(self):
        certification = self.get_object()
        if self.request.user == certification.teacher_id.user:
            return True
        return False
    
class CertificationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Certification
    success_url = "/certifications/"

    def test_func(self):
        certification = self.get_object()
        if self.request.user == certification.teacher_id.user:
            return True
        return False

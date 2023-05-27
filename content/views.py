from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Content
from course.models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

class ContentListView(ListView):
    model = Content
    template_name = "content/content_list.html"
    context_object_name = "contents"

    def get_queryset(self):
        course_id = get_object_or_404(Course, pk=self.kwargs.get('course_pk'))
        # content = self.get_object()
        return Content.objects.filter(c_id=course_id)
    
    
class ContentDetailView(LoginRequiredMixin, DetailView):
    model = Content
    template_name="content/content_detail.html"
    context_object_name = "content"
    

class ContentCreateView(LoginRequiredMixin, CreateView):
    model = Content
    fields = ["video", "content_title", "notes"]
    success_url = "/"

    def form_valid(self, form):
        course_id = get_object_or_404(Course, pk=self.kwargs.get('course_pk'))
        form.instance.c_id = course_id
        return super().form_valid(form)
    
class ContentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Content
    fields = ["video", "content_title", "notes"]
    success_url = "/"

    def form_valid(self, form):
        course_id = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        form.instance.c_id = course_id
        return super().form_valid(form)
    
    def test_func(self):
        content = self.get_object()
        if self.request.user == content.c_id.owner.user:
            return True
        return False
    
class ContentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Content
    success_url = "/"

    def test_func(self):
        content = self.get_object()
        if self.request.user == content.c_id.owner.user:
            return True
        return False

class OwnedContentListView(ListView):
    model = Content
    template_name = "content/owned_content_list.html"
    context_object_name = "contents"

    def get_queryset(self):
        course_id = get_object_or_404(Course, pk=self.kwargs.get('course_pk'))
        # content = self.get_object()
        return Content.objects.filter(c_id=course_id)
    
def ownedContentListView(request, course_pk):
    course_id = get_object_or_404(Course, pk=course_pk)
    # content = self.get_object()
    contents =  Content.objects.filter(c_id=course_id)
    data = {}
    data["contents"] = contents
    data["course_id"] = course_id.id

    return render(request, "content/owned_content_list.html", data)

class OwnedContentDetailView(LoginRequiredMixin, DetailView):
    model = Content
    template_name="content/owned_content_detail.html"
    context_object_name = "content"
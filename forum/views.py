from django.shortcuts import render, get_object_or_404
from .models import Forum, Message
from course.models import Course
from .forms import MessageForm
from enrollment.models import Enrollment
from users.models import Student
# Create your views here.

def view_forum(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course_forum = get_object_or_404(Forum, course_id=course)
    messages = Message.objects.filter(forum_id=course_forum)
    student = get_object_or_404(Student, user=request.user)
    enrollment = Enrollment.objects.filter(student_id=student).filter(course_id=course).first()
    data = {"messages": messages}   
    
    data["Eid"] = enrollment

    if(request.method == "POST"):
        form = MessageForm(request.POST)
        if form.is_valid():
            form.instance.forum_id = course_forum
            form.instance.writer = request.user
            form.save()
            form = MessageForm
            data["form"] = form
            return render(request, 'forum/course_forum.html', data)
    else:
        form = MessageForm
        data["form"] = form
        return render(request, 'forum/course_forum.html', data)


        
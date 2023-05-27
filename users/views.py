from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm
from certification.models import Certification
from .models import Teacher

# Create your views here.


def register(request):
    if (request.method == "POST"):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def home(request):
    return render(request, "users/home.html")


def profile(request):
    if (request.method == "POST"):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
    else:
        form = UserUpdateForm(instance=request.user)
        return render(request, "users/profile.html", {"form": form})


def instructorInfo(request, pk):
    instructor = Teacher.objects.filter(pk=pk).first()
    certifications = Certification.objects.filter(teacher_id=instructor)

    context = {"instructor": instructor, "certifications": certifications}

    return render(request, 'users/instructor_info.html', context)


def contact(response):
    return render(response, 'users/contact.html', {})


def about(response):
    return render(response, 'users/about.html', {})


def home(respone):
    return render(respone, 'users/home.html', {})

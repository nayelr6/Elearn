from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import CoursePayment
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Student, Teacher
from course.models import Course
from enrollment.models import Enrollment
from exam.models import Exam
from questions.models import Question
from takes_exam.models import takes_exam
from .forms import Withdrawal

# Create your views here.
class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = CoursePayment
    fields = []
    success_url = "/purchased/"

    def form_valid(self, form):
        form.instance.student = Student.objects.filter(user=self.request.user).first()
        enrolled_course =  get_object_or_404(Enrollment, pk=self.kwargs.get('pk'))
        form.instance.course = Course.objects.filter(id=enrolled_course.course_id.id).first()
        form.instance.teacher = Teacher.objects.filter(user=enrolled_course.course_id.owner.id).first()
        form.instance.amount = Course.objects.filter(id=enrolled_course.course_id.id).first().fees
        return super().form_valid(form)
    
class PaymentListView(LoginRequiredMixin, ListView):
    model = CoursePayment
    context_object_name = "object"

    def get_queryset(self):
        student_id = get_object_or_404(Student, user=self.request.user)
        purchases = CoursePayment.objects.filter(student=student_id)

        return purchases

class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = CoursePayment

class StudentExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = "coursePayment/exam_list.html"
    context_object_name = "exams"

    def get_queryset(self):
        course_id = get_object_or_404(Course, pk=self.kwargs.get('course_pk'))
        return Exam.objects.filter(course=course_id)

class StudentExamDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = "coursePayment/exam_detail.html"
    context_object_name = "exam"

def st_exam_questions(request, course_pk, pk):
    exam = get_object_or_404(Exam, id=pk)
    questions = Question.objects.filter(exam=exam)

    questions_list = []
    for question in questions:
        question_info = {}
        question_info["qs"] = question.qs
        question_info["op1"] = question.option_1
        question_info["op2"] = question.option_2
        question_info["op3"] = question.option_3
        question_info["op4"] = question.option_4
        question_info["correct"] = question.correct
        questions_list.append(question_info)

    return JsonResponse({
        'data' : questions_list,
    })

def st_exam(request, course_pk, pk):
    user = request.user
    st = Student.objects.filter(user=user).first()
    course = get_object_or_404(Course, pk=course_pk)
    exam = Exam.objects.filter(pk=pk)
    exam_info = {"course" : course}
    user_exams = takes_exam.objects.filter(student=st)
    selected_exam = None
    for user_exam in user_exams:
        if user_exam.exam.id == pk:
            selected_exam = user_exam

    if selected_exam != None:
        return redirect("exam-result", pk=pk, course_pk=course_pk)
    else:
        return render(request, "coursePayment/st_takes_exam.html", exam_info)

def save_quiz_view(request, course_pk, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
        user = request.user
        st = Student.objects.filter(user=user).first()
        exam = Exam.objects.filter(pk=pk).first()
        data=request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        questions = []

        for k in data_.keys():
            question = Question.objects.get(qs=k)
            questions.append(question)
        
        score = 0
        for q in questions:
            a_selected = request.POST.get(q.qs)
            if a_selected == q.correct:
                score += 1


        feedback = ""
        if score == len(questions):
            feedback="Excellent"
        elif score >= len(questions)*0.8:
            feedback="Well done"
        elif score >= len(questions)*0.6:
            feedback="Needs improvement"
        else:
            feedback="Please review the material again"

        takes_exam.objects.create(student=st, exam=exam, feedback=feedback, marks=score)
    
        response = {'status': 1, 'message': "OK", "your_url": "exam-result", "course_pk": course_pk, "pk": pk}

        return JsonResponse(response)
    
def exam_result(request, course_pk, pk):
    course = get_object_or_404(Course, pk=course_pk)
    exam_info = {"course" : course}
    st = Student.objects.get(user=request.user)
    user_exams = takes_exam.objects.filter(student=st)
    selected_exam = None
    for user_exam in user_exams:
        if user_exam.exam.id == pk:
            selected_exam = user_exam

    if selected_exam != None:
        exam_info["feedback"] = selected_exam.feedback
        exam_info["marks"] = selected_exam.marks

        return render(request, "coursePayment/exam_result.html", exam_info)
    else:
        return redirect("st-exam", pk=pk, course_pk=course_pk)
    
def payment_update_view(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    payments = CoursePayment.objects.filter(course=course)

    if request.method == "POST":
        form = Withdrawal(request.POST)

        payments.update(amount=0)

        return redirect("owned-course-detail", course_pk)
        
    else:
        form = Withdrawal()
        total_amount = 0
        for payment in payments:
            if payment.amount > 0:
                total_amount += payment.amount

        return render(request, "coursePayment/withdraw.html", {"form": form, "amount": total_amount})
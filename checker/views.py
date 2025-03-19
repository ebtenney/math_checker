from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Question, Student_Work

def index(request):
    latest_question_list = Question.objects.order_by("-textbook")[:5]
    template = loader.get_template("checker/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "checker/detail.html", {"question": question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def student_work_list(request):
    student_work_list = Student_Work.objects.all()
    return render(request, 'checker/student_work_list.html', {'student_work_list': student_work_list})

def question_list(request):
    question_list = Question.objects.all()
    return render(request, 'checker/question_list.html', {'question_list': question_list})

def upload_page(request):
    return render(request, 'checker/BasicSite.html')
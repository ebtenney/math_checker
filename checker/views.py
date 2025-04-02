from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Question, Student_Work, Student_Work_PDF

def signup_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            user = User.objects.create_user(username, None, password1)
            user.save()
            auth = authenticate(request, username=username, password=password1)

            if auth is not None:
                login(request, auth)
                return redirect('index')
            else:
                return redirect('login')

        else:
            return render(request, 'authenticate/signup.html', {'nomatch': True})

    return render(request, 'authenticate/signup.html')

def auth_view(request):
    """ Login page view """
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"] 
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'authenticate/login.html', {'error_message': True})

    return render(request, 'authenticate/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def account_view(request):
    """ Account page view """
    return render(request, 'authenticate/account.html', {'audio_files': request.user.audiofile_set.all()})

def home_view(request):
    """ Homepage View """
    return render(request, 'checker/index.html')

def index(request):
    latest_question_list = Question.objects.order_by("-textbook")[:5]
    template = loader.get_template("checker/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))

@login_required
def upload_pdf(request):
    """ pdf upload page view"""
    max_file_size = 25 * 1024 * 1024  # 25MB in bytes

    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        if pdf_file is not None:
            if pdf_file.size < max_file_size:
                pdf = Student_Work_PDF.objects.create(pdf=pdf_file,
                                                 owner=request.user)
                pdf.name = pdf.pdf.name.replace('uploads/', '')
                pdf.save()
                # TODO: send to transcription api
                # handle_uploaded_audio(audio, audio.audio.path)

                return redirect('results', pdf.id)
            else:
                return render(request, 'checker/upload.html',
                              {'file_too_large': True})
        else:
            return render(request, 'checker/upload.html',
                          {'no_file': True})

    return render(request, 'checker/upload.html')


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
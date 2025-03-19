from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('student-work/', views.student_work_list, name='student_work_list'),
    path('questions/', views.question_list, name='question_list'),
]
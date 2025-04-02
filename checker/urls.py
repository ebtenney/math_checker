from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("home/", views.index, name="home"),
    path('student-work/', views.student_work_list, name='student_work_list'),
    path('questions/', views.question_list, name='question_list'),
    path('upload/', views.upload_page, name='upload_page'),
    path('upload/', views.upload_pdf, name='upload_pdf'),

    
    path('accounts/login/', views.auth_view, name="login"),
    path('accounts/signup/', views.signup_view, name="signup"),
    path('account/', views.account_view, name="account"),
    path('accounts/logout/', views.logout_view, name="logout"),
]
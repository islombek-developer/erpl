from django.urls import path
from .views import (
    StudentDashboardView, StudentGroupView, StudentLessonsView, 
    HomeworkView, HomeDetailView, ProfileView, EditProfileView, 
    ResetPasswordView,HomeworkListView,student_total_oylik
)

app_name = 'students'
urlpatterns = [
    path('dashboard/', StudentDashboardView.as_view(), name='dashboard'),
    path('groups/', StudentGroupView.as_view(), name='groups'),
    path('resed_password/', ResetPasswordView.as_view(), name='resed_password'),
    path('profil-students/', ProfileView.as_view(), name='profil'),
    path('lessons/<int:group_id>/', StudentLessonsView.as_view(), name='lessons'),
    path('homework/<int:lesson_id>/', HomeworkView.as_view(), name='homework'),
    path('edit/<int:id>/', EditProfileView.as_view(), name='edit'),
    path('homework-detail/<int:lesson_id>/', HomeDetailView.as_view(), name='homework_detail'),
    path('homeworks/<int:lesson_id>/', HomeworkListView.as_view(), name='homework_list'),
    path('student/<int:student_id>/payments/', student_total_oylik, name='student_total_oylik'),
  ]

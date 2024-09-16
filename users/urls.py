from django.urls import path
from .views import (LoginView, RegisterView,ProfileView,EditProfileView,Create,TeamStudentListView,TolovGroupsView,
                    LogautView,GroupsView,StudentView,EditStudentView,Delete,StudentByTeam,TeacherView,TeacherAdminMonthStudent,
                    ResetPasswordView,AdminDashboardView,CreateTeamView,DeleteTeamView,DeleteTeacher,TolovTeacherListView)

app_name = 'users'


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogautView.as_view(), name='logout'),
    path('create/', Create.as_view(), name='create'),
    path('profil/', ProfileView.as_view(), name='profil'),
    path('dashboard/', AdminDashboardView.as_view(), name='dashboard'),
    path('edit/<int:id>/', EditProfileView.as_view(), name='edit'),
    path('group/', GroupsView.as_view(), name='groups'),
    path('students/', StudentView.as_view(), name='students'),
    path('get-by-students/<int:id>/', StudentByTeam.as_view(), name='students_by'),
    path('edit-student/<int:id>/', EditStudentView.as_view(), name='edit_student'),
    path('delete/<int:id>/', Delete.as_view(), name='delete'),
    path('resed-password', ResetPasswordView.as_view(), name='resed_password'),
    path('create-team/', CreateTeamView.as_view(), name='create_team'),
    path('teacher/', TeacherView.as_view(), name='teacher'),
    path('teacher-tolov/', TolovGroupsView.as_view(), name='teacher_tolov'),
    path('delete-team/<int:id>/', DeleteTeamView.as_view(), name='delete_team'),
    path('delete-teacher/<int:id>/', DeleteTeacher.as_view(), name='delete_teacher'),
    path('month-teacher/<int:id>/', TeacherAdminMonthStudent.as_view(), name='month_teacher'),
    path('team/student/create/', TeamStudentListView.as_view(), name='create_student'),
    path('tolov-teacher/<int:id>/', TolovTeacherListView.as_view(), name='tolov_teacher'),
]
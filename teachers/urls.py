from django.urls import path
from .views import  (TeacherView,TeacherTimesView,TeacherGroup,TeacherHomeworks,CreateMonthView,TolovListView,DeleteStudent,
                     TeacherStudentsView,ProfileView,EditProfileView,ResetPasswordView,DeleteMonthView,CreateTolovView,
                     TeacherCreateLessonView,TeacherStudentLeson,DavomatListView,TeacherMonthStudent,TeamStudentListView,
                     DateCreateView,StudentsDateView)
from .views import present_students,create_attendance
app_name = 'teachers'


urlpatterns = [
    path('dashboard/',TeacherView.as_view(),name='dashboard'),
    path('guruhlarim/',TeacherTimesView.as_view(),name='guruhlarim'),
    path('resed_password/',ResetPasswordView.as_view(),name='resed_password'),
    path('profil-teacher/',ProfileView.as_view(),name='profil'),
    path('guruh/<int:team_id>/',TeacherGroup.as_view(),name='guruh'),
    path('homework/<int:team_id>/',TeacherHomeworks.as_view(),name='homeworks'),
    path('edit/<int:id>/',EditProfileView.as_view(),name='edit'),
    path('student/<int:team_id>/',TeacherStudentsView.as_view(),name='student'),
    path('create/<int:team_id>/',TeacherCreateLessonView.as_view(),name='create'),
    path('stydents/<int:id>/',TeacherStudentLeson.as_view(),name='stydents'),
    path('davomat/<int:id>/', DavomatListView.as_view(), name='davomat_list'),
    path('month/<int:id>/', TeacherMonthStudent.as_view(), name='month_student'),
    path('create-month/<int:team_id>/', CreateMonthView.as_view(), name='createmont'),
    path('delete-month/<int:id>', DeleteMonthView.as_view(), name='deletemont'),
    path('create-tolov/<int:month_id>/', CreateTolovView.as_view(), name='create_tolov'),
    path('tolov-list/<int:id>/', TolovListView.as_view(), name='tolov_list'),
    path('delete-student-list/<int:id>/', DeleteStudent.as_view(), name='delete_student'),
    path('team/student/create/', TeamStudentListView.as_view(), name='create_student'),
    path('create-date/<int:team_id>/', DateCreateView.as_view(), name='create_date'),
    path('teachers/date-list/<int:team_id>/', StudentsDateView.as_view(), name='students_date_list'),
    path('present-students/<int:date_id>/', present_students, name='present_students'),
    path('create-attendance/<int:date_id>/', create_attendance, name='create_attendance'),
]
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from users.permissionmixin import StudentRequiredMixin
from django.views import View
from users.models import Student, Team,User
from .forms import HomeworkForm,DavomatForm
from .models import Lesson, Homework,Davomat
from users.forms import ProfileForm,ResetPasswordForm

class StudentDashboardView(StudentRequiredMixin, View):
    def get(self, request):
        return render(request, 'students/dashboard.html')

class StudentGroupView(StudentRequiredMixin, View):
    def get(self, request):
        student = Student.objects.get(user=request.user)
        return render(request, 'students/guruhlarim.html', context={"student":student})
    
class HomeworkListView(View):
    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        homeworks = Homework.objects.filter(lesson=lesson)
        return render(request, 'students/homework.html', {'lesson': lesson, 'homeworks': homeworks})

class StudentLessonsView(StudentRequiredMixin, View):
    def get(self, request, group_id):
        team = get_object_or_404(Team, id=group_id)
        lessons = team.lesson.all()
        return render(request, 'students/lessons.html', context={"lessons":lessons})
    

class HomeworkView(StudentRequiredMixin, View):
    def get(self, request, lesson_id):
        form = HomeworkForm()
        return render(request, 'students/homework.html', context={"form":form})
    
    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        student = get_object_or_404(Student, user=request.user)

        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            homework = Homework()
            homework.lesson = lesson
            homework.student = student
            homework.description = form.cleaned_data['description']
            homework.homework_file = form.cleaned_data['homework_file']
            homework.save()

            lesson.homework_status = True
            lesson.save()

            return redirect('students:dashboard')
        form = HomeworkForm()
        return render(request, 'students/homework.html', context={"form":form})
        
class HomeDetailView(StudentRequiredMixin,View):
    def get(self,request,lesson_id):
        lesson = get_object_or_404(Lesson,id=lesson_id)
        student = get_object_or_404(Student , user=request.user)
        homework = Homework.objects.filter(lesson=lesson , student=student).first()
        return render(request,'students/homedetail.html',{'homework':homework})
    
class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user
        return render(request,'students/profil.html',context={"user":user})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        form = ProfileForm(instance=user)
        return render(request, 'students/edit.html', {'form': form})

    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('students:profil')  
        return render(request, 'students/edit.html', {'form': form})

class ResetPasswordView(LoginRequiredMixin,View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'students/reset_password.html', {'form':form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = request.user
            user.set_password(new_password)
            user.save()
            return redirect('/')
        form = ResetPasswordForm()
        return render(request, 'students/reset_password.html', {'form':form})
    
class DavomatListView(View):
    def get(self, request):
        davomat_list = Davomat.objects.all()
        form = DavomatForm()
        return render(request, 'students/davomat_list.html', {'davomat_list': davomat_list, 'form': form})

    def post(self, request):
        form = DavomatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('davomat_list')
        davomat_list = Davomat.objects.all()
        return render(request, 'students/davomat_list.html', {'davomat_list': davomat_list, 'form': form})

def student_total_oylik(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    total_oylik = Tolov.total_oylik_for_student(student_id)  
    tolovlar = Tolov.objects.filter(student=student)
    
    context = {
        'student': student,
        'total_oylik': total_oylik,
        'tolovlar': tolovlar,
    }
    return render(request, 'students/student_oylik.html', context)

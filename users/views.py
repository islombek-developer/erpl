from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from .forms import LoginForm, RegisterForm,ProfileForm,StudentEditForm,TeamForm,ResetPasswordForm,StudentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User,Student,Team,Teacher
from .permissionmixin import AdminRequiredMixin,StudentRequiredMixin,TeacherRequiredMixin
from django.db.models import Q
from django.db import IntegrityError
from teachers.models import Tolov,Month
from django.db.models import Sum

class TeamStudentListView(View):
    def get(self, request):
        form = StudentForm()
        return render(request, 'users/create_student.html', {'form': form})

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                student = form.save()
                return redirect('/dashboard')  
            except IntegrityError:
                form.add_error('username', 'Username already exists')
        return render(request, 'users/create_student.html', {'form': form})     

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_role=='student':
                    return redirect('students/dashboard')
                elif user.user_role=='teacher':
                    return redirect('teachers/dashboard')
                elif user.user_role=='admin':
                    return redirect('/dashboard')

        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})


class RegisterView(AdminRequiredMixin, View):
    
    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            
            if user.user_role == 'student':
                Student.objects.create(user=user)
                
            elif user.user_role == 'teacher':
                newteacher = Teacher.objects.create(user=user)
                
                if form.cleaned_data['team']:
                    team = form.cleaned_data['team']
                    team.teacher = newteacher
                    team.save()
            
            return redirect('/dashboard')
        return render(request, 'users/register.html', {'form': form})

class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user
        return render(request,'users/profil.html',context={"user":user})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        form = ProfileForm(instance=user)
        return render(request, 'users/edit.html', {'form': form})

    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/profil')
        return render(request, 'users/edit.html', {'form': form})
        
class Create(View):

    def get(self, request):
        form = ProfileForm()
        return render(request, 'users/create.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            return redirect('/students')

        form = ProfileForm()
        return render(request, 'users/create.html', {'form': form})

class LogautView(View):
    def get(self,request):
        logout(request)
        return redirect("/")

class GroupsView(View):
    def get(self,request):
        teams = Team.objects.all()
        return render(request,'users/groups.html',{"teams":teams})

class CreateTeamView(View):
    def get(self, request):
        form = TeamForm()
        return render(request, 'users/create1.html', {'form': form})

    def post(self, request):
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            return redirect('/dashboard') 
        return render(request, 'users/create1.html', {'form': form})

class DeleteTeamView(AdminRequiredMixin, View):
    def get(self, request, id):
        team = get_object_or_404(Team, id=id)
        team.delete()
        return redirect('/dashboard')

class StudentView(AdminRequiredMixin, View):
    def get(self, request):
        search_term = request.GET.get('search', '').strip()
        if search_term:
            students = Student.objects.filter(
                Q(user__name__icontains=search_term) | 
                Q(team__name__icontains=search_term)
            )
        else:
            students = Student.objects.all()
        
        return render(request, 'users/student.html', {"students": students})

class StudentByTeam(AdminRequiredMixin,View):
    def get(self,request,id):
        team = get_object_or_404(Team,id=id)
        students = team.students.all()
        return render(request,'users/student.html',{"students":students})


class EditStudentView(AdminRequiredMixin, View):
    def get(self, request, id):
        student = get_object_or_404(Student, id=id)
        form = StudentEditForm(instance=student)
        return render(request, 'users/edit.html', {'form': form})

    def post(self,request,id):
        student = get_object_or_404(Student, id=id)

        form = StudentEditForm(request.POST,instance=student)
        if form.is_valid():
            form.save()
            return redirect('/students')
        form = StudentEditForm(instance=student)
        return render(request, 'users/edit.html', {'form': form})

class Delete(AdminRequiredMixin,View):
    def get(self,request,id):
        student = get_object_or_404(Student, id=id)
        user = User.objects.get(username=student.user.username)
        student.delete()
        user.delete()
        return redirect('/dashboard')



class ResetPasswordView(LoginRequiredMixin,View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'users/reset_password.html', {'form':form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = request.user
            user.set_password(new_password)
            user.save()
            return redirect('/')
        form = ResetPasswordForm()
        return render(request, 'users/reset_password.html', {'form':form})


class AdminDashboardView(AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/dashboard.html')
    
class TeacherView(View):
    def get(self,request):
        teams = Teacher.objects.all()
        return render(request,'users/teachers.html',{"teams":teams})

class DeleteTeacher(AdminRequiredMixin,View):
    def get(self,request,id):
        teacher = get_object_or_404(Teacher, id=id)
        user = User.objects.get(username=teacher.user.username)
        teacher.delete()
        user.delete()
        return redirect('/teacher')

class TolovGroupsView(View):
    def get(self,request):
        teams = Team.objects.all()
        return render(request,'users/groups_tolov.html',{"teams":teams})

class TeacherAdminMonthStudent(View):
    def get(self, request, id):
        month = get_object_or_404(Team, id=id)
        months = month.tolov_set.all()
        return render(request, 'users/month_tolov.html', context={
            'month': month,
            'months': months,
        })


class TolovTeacherListView(View):
    def get(self, request, id):
        month = get_object_or_404(Month, id=id)
        team = month.team
        students = team.students.all()

        tolovs = Tolov.objects.filter(month=month, student__team=team)

        total_oylik = tolovs.aggregate(total_oylik=Sum('oylik'))['total_oylik'] or 0

        context = {
            'month': month,
            'students': students,  
            'tolovs': tolovs,  
            'total_oylik': total_oylik,
            'team': team,
        }
        return render(request, 'users/tolov_teacher.html', context)
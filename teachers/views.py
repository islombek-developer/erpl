from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404,redirect
from  users.permissionmixin import TeacherRequiredMixin
from  django.views import  View
from  users.models import Teacher,Student,User
from  students.models import Lesson,Team,Homework,Davomat,Date
from users.forms import ProfileForm,ResetPasswordForm
from .forms import CreateLessonForm,DavomatForm,TeacherProfileForm
from django.urls import reverse
from users.forms import StudentForm
from django.db import IntegrityError

class TeamStudentListView(View):
    def get(self, request):
        form = StudentForm()
        return render(request, 'teachers/create_student.html', {'form': form})

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                student = form.save()
                return redirect('/teachers/dashboard')  
            except IntegrityError:
                form.add_error('username', 'Username already exists')
        return render(request, 'teachers/create_student.html', {'form': form})   


class TeacherView(TeacherRequiredMixin,View):
    def get(self,request):
        return render(request,'teachers/dashboard.html')

class TeacherTimesView(TeacherRequiredMixin,View):
    def get(self,request):
        teacher = get_object_or_404(Teacher,user=request.user)
        teams = teacher.teacher.all()
        return render(request,'teachers/guruhlarim.html',{"teams":teams})

class TeacherGroup(TeacherRequiredMixin,View):
    def get(self,request,team_id):
        team = get_object_or_404(Team,id=team_id)
        lessons = team.lesson.all()
        return render(request,'teachers/guruh.html',{'team':team,'lessons':lessons})

class TeacherHomeworks(TeacherRequiredMixin,View):
    def get(self,request,team_id):
        team = get_object_or_404(Team,id=team_id)
        lessons = team.homeworks.all()
        return render(request,'teachers/guruh.html',{'team':team,'lessons':lessons})

class TeacherStudentsView(TeacherRequiredMixin,View):
    def get(self,request,team_id):
        team = get_object_or_404(Team,id=team_id)
        student = team.students.all()
        return render(request,'teachers/student.html',{'team':team,'student':student})

class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user
        return render(request,'teachers/profil.html',context={"user":user})

class TeacherHomevorkStudent(TeacherRequiredMixin,View):
    def get(self,request,team_id):
        team = get_object_or_404(Team,id=team_id)
        lessons = team.lesson.all()
        return render(request,'teachers/guruh.html',{'team':team,'lessons':lessons})

class EditProfileView(LoginRequiredMixin, View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        form = TeacherProfileForm(instance=user)
        return render(request, 'teachers/edit.html', {'form': form})

    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        form = TeacherProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('teachers:profil')  
        return render(request, 'teachers/edit.html', {'form': form})

class ResetPasswordView(LoginRequiredMixin,View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'teachers/reset_password.html', {'form':form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = request.user
            user.set_password(new_password)
            user.save()
            return redirect('/')
        form = ResetPasswordForm()
        return render(request, 'teachers/reset_password.html', {'form':form})

from .models import Tolov, Month
from django.db.models import Sum

class TeacherCreateLessonView(TeacherRequiredMixin, View):
    def get(self, request, team_id):
        form = CreateLessonForm()
        return render(request, 'teachers/create_lesson.html', {'form': form})

    def post(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        form = CreateLessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = Lesson(
                team=team,
                title=form.cleaned_data['title'],
                lesson_file=form.cleaned_data['lesson_file'],
            )
            lesson.save()
            url = reverse('teachers:homeworks', args=[team_id])
            return redirect(url)
        return render(request, 'teachers/create_lesson.html', {'form': form})


class TeacherStudentLeson(TeacherRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        lesson_id = kwargs.get('id')  
        lesson = get_object_or_404(Lesson, id=lesson_id)
        homeworks = Homework.objects.filter(lesson=lesson).select_related('student', 'team')
        return render(request, 'teachers/students.html', {'homeworks': homeworks, 'lesson': lesson})

class TeacherHomeworkListView(TeacherRequiredMixin, View):
    def get(self, request):
        lessons = Lesson.objects.filter(team__teacher=request.user.teacher)
        homeworks = Homework.objects.filter(lesson__in=lessons).select_related('student__user', 'lesson')
        return render(request, 'teachers/homework_list.html', {'homeworks': homeworks})




class DavomatListView(View):
    model = Davomat
    template_name = 'davomat_list.html'
    
    def get_queryset(self):
        team_id = self.kwargs['team_id']
        return Davomat.objects.filter(student__team_id=team_id)


from django.views import View
from .models import Month
from .forms import MonthForm

class TeacherMonthStudent(TeacherRequiredMixin,View):
    def get(self, request, id):
        month = get_object_or_404(Team, id=id)
        months = month.tolov_set.all()
        return render(request, 'teachers/month.html', context={
            'month': month,
            'months': months,
        })


class CreateMonthView(View):
    def get(self, request, *args, **kwargs):
        team_id = kwargs.get('team_id')
        form = MonthForm()
        return render(request, 'teachers/create_month.html', {'form': form, 'team_id': team_id})

    def post(self, request, *args, **kwargs):
        team_id = kwargs.get('team_id')
        team = Team.objects.get(id=team_id)

        form = MonthForm(request.POST)
        if form.is_valid():
            month = form.save(commit=False)
            month.team = team  
            month.save()
            return redirect('/teachers/guruhlarim/')
        
        return render(request, 'teachers/create_month.html', {'form': form, 'team_id': team_id})
    
class DeleteMonthView(View):
    def get(self, request, id, *args, **kwargs):
        month = get_object_or_404(Month, id=id)
        month.delete()
        return redirect('/teachers/guruhlarim/')  
    
from django.db.models import Sum

class TolovListView(View):
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
        return render(request, 'teachers/tolov_list.html', context)
        
from .forms import TolovForm

class CreateTolovView(View):
    def get(self, request, month_id):
        month = get_object_or_404(Month, id=month_id)
        students = Student.objects.filter(team=month.team)
        form = TolovForm()
        
        context = {
            'form': form,
            'month': month,
            'students': students,
        }
        return render(request, 'teachers/create_tolov.html', context)

    def post(self, request, month_id):
        month = get_object_or_404(Month, id=month_id)
        students = Student.objects.filter(team=month.team)

        for student in students:
            payment_amount = request.POST.get(f'payment_{student.id}')
            if payment_amount:
                # Check if a record already exists for this student and month
                existing_tolov = Tolov.objects.filter(student=student, month=month).first()
                if existing_tolov:
                    # Update the existing record
                    existing_tolov.oylik = payment_amount
                    existing_tolov.save()
                else:
                    # Create a new record
                    Tolov.objects.create(student=student, month=month, oylik=payment_amount)
        
        return redirect('/teachers/guruhlarim/')

    def post(self, request, month_id):
        month = get_object_or_404(Month, id=month_id)
        form_data = request.POST
        students = Student.objects.filter(team=month.team)

        for student in students:
            payment_amount = form_data.get(f'payment_{student.id}')
            if payment_amount:
                Tolov.objects.create(
                    month=month,
                    team=month.team,
                    student=student,
                    oylik=payment_amount  
                )
        
        return redirect('/teachers/guruhlarim/')

class DeleteStudent(View):
    def get(self,request,id):
        student = get_object_or_404(Student, id=id)
        user = User.objects.get(username=student.user.username)
        student.delete()
        user.delete()
        return redirect('/teachers/dashboard')


class DateCreateView(View):
    def get(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        return render(request, 'teachers/create_date.html', {'team': team})

    def post(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        Date.objects.create(
            team=team
        )
        
        return redirect('/teachers/dashboard')

class StudentsDateView(TeacherRequiredMixin, View):
    def get(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        dates = Date.objects.filter(team=team)
        return render(request, 'teachers/date_list.html', {'team': team, 'dates': dates})

def present_students(request, date_id):
    date = get_object_or_404(Date, id=date_id)
    present_students = Davomat.objects.filter(date=date, status=True)

    context = {
        'date': date,
        'present_students': present_students,
    }
    return render(request, 'teachers/present.html', context)




def create_attendance(request, date_id):
    date = get_object_or_404(Date, id=date_id)
    # Filter students based on the team associated with the date
    students = Student.objects.filter(team=date.team)
    
    if request.method == 'POST':
        # Clear previous records for the given date and team
        Davomat.objects.filter(date=date, team=date.team).delete()

        for student in students:
            # Get the status from the form
            status = request.POST.get(f'attendance_{student.id}')
            # Determine if the checkbox was checked
            status_value = True if status == 'on' else False
            Davomat.objects.create(student=student, date=date, team=date.team, status=status_value)

        return redirect('/teachers/guruhlarim/')  

    # Get existing attendance records for the specific date and team
    existing_attendance = Davomat.objects.filter(date=date, team=date.team)
    attendance_ids = [attendance.student.id for attendance in existing_attendance]

    context = {
        'date': date,
        'students': students,
        'attendance_ids': attendance_ids,
    }
    return render(request, 'teachers/davomat_list.html', context)
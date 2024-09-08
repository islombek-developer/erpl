from django import forms
from students.models import Davomat ,Lesson,Date
from .models import Month, Tolov
from users.models import User

class TeacherProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "Name"}))
    phone_number = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "Phone Number"}))
    first_name = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "Last Name"}))
    jobs = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "Jobs"}))
    address = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "address"}))
    email = forms.CharField(widget=forms.EmailInput({"class": "form-control", "placeholder": "address"}))
    image = forms.ImageField(widget=forms.FileInput({"class": "form-control", "placeholder": "image"}))
    
    class Meta:
        model = User
        fields = ('username', 'phone_number','address', 'first_name', 'last_name','image','email','jobs')

class MonthForm(forms.ModelForm):
    class Meta:
        model = Month
        fields = [ 'month']
        widgets = {
            'month': forms.TextInput(attrs={'placeholder': 'Enter month name'}),
        }

class TolovForm(forms.ModelForm):
    class Meta:
        model = Tolov
        fields = ['student',  'oylik']
        widgets = {
            'oylik': forms.NumberInput(attrs={'placeholder': 'Enter the amount'}),
        }


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [ 'title', 'homework_status', 'lesson_file']
    
    title = forms.CharField(widget=forms.TextInput({'class': 'form-control'}))


class DavomatForm(forms.ModelForm):
    class Meta:
        model = Davomat
        fields = [ 'student', 'status','date'] 
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class DateForm(forms.ModelForm):
    class Meta:
        model = Date
        fields = '__all__' 

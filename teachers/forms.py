from django import forms
from students.models import Davomat ,Lesson,Date
from .models import Month, Tolov

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
        fields = ['student', 'month', 'oylik']
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

from django import forms
from .models import User,Student,Team,Teacher
from django.core.exceptions import ValidationError

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'end_date', 'teacher']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput({"class": "form-control", "placeholder": "Password"}))

class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "Name"}))
    phone_number = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "Phone Number"}))
    first_name = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "Last Name"}))
    password = forms.CharField(widget=forms.PasswordInput({"class": "form-control", "placeholder": "Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput({"class": "form-control", "placeholder": "Confirm Password"}))
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'first_name', 'last_name', 'password', 'confirm_password', 'user_role', 'team')

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:    
            raise forms.ValidationError("Passwords do not match")
        return password

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            if self.cleaned_data['user_role'] == 'teacher':
                teacher = Teacher.objects.create(user=user)
                if self.cleaned_data['team']:
                    team = self.cleaned_data['team']
                    team.teacher = teacher
                    team.save()
        return user


class StudentForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "Username"}))
    first_name = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "Last Name"}))
    phone_number = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": "Phone Number"}))
    date_of_birth = forms.DateField(widget=forms.DateInput({"class": "form-control", "placeholder": "Date of Birth"}))
    password = forms.CharField(widget=forms.PasswordInput({"class": "form-control", "placeholder": "Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput({"class": "form-control", "placeholder": "Confirm Password"}))
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = Student
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'password', 'confirm_password', 'team')

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone_number=self.cleaned_data['phone_number'],
            password=self.cleaned_data['password'],
            user_role='student'  # Set the role to student
        )
        student = Student.objects.create(
            user=user,
            date_of_birth=self.cleaned_data['date_of_birth'],
            team=self.cleaned_data['team'] if self.cleaned_data['team'] else None
        )
        return student

class ProfileForm(forms.ModelForm):
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
        fields = ('username', 'phone_number','address', 'first_name', 'last_name','image','email','jobs','user_role')

class StudentEditForm(forms.ModelForm):
    end_date = forms.DateField(widget=forms.TextInput({"class": "form-control", "placeholder": "Name"}))
    class Meta:
        model = Student
        fields = ('team','end_date')

class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput({"class": "form-control", "placeholder": "Old Password"}))
    new_password = forms.CharField(widget=forms.PasswordInput({"class": "form-control", "placeholder": "New Password"}))
    confirrm_password = forms.CharField(widget=forms.PasswordInput({"class": "form-control", "placeholder": "Confirm Password"}))

    def clean_confirm_password(self):
        new_password = self.cleaned_data['new_password']
        new_password = self.cleaned_data['confirm_password']

        if new_password !=confirm__password:
            raise forms.ValidationError("passwords dont mach")
        
        return confirm_password

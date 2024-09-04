from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_ROLE =(
        ('student','student'),
        ('teacher','teacher'),
        ('admin','admin'),
    )
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/default.jpg')
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    jobs = models.CharField(max_length=200, blank=True, null=True)
    user_role = models.CharField(max_length=100,choices=USER_ROLE,default="student")

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_of = models.DateField(null=True,blank=True )

    def __str__(self):
        return self.user.username

    

class Team(models.Model):
    name=models.CharField(max_length=70, unique=True)
    date_created=models.DateField(auto_now_add=True)
    end_date=models.DateField(blank=True, null=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name='teacher',null=True,blank=True)

    def __str__(self):
        return self.name
   

class Student(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth=models.DateField(blank=True, null=True)
    team=models.ForeignKey(Team, on_delete=models.CASCADE, related_name='students',null=True,blank=True)

    def __str__(self):
        return self.user.first_name
    

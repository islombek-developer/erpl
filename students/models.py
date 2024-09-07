from django.db import models
from users.models import Team,Student,Teacher
from django.core.validators import MaxValueValidator,FileExtensionValidator

class Lesson(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='lesson')
    title = models.CharField(max_length=100, unique=True)
    date = models.DateField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    homework_status = models.BooleanField(default=False)
    lesson_file = models.FileField(upload_to='lesson/',  null=True,blank=True)
    video = models.FileField(
        upload_to='video/', 
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mp3', 'AVI', 'WMV'])],
        null=True,
        blank=True
    )


    class Meta:
        unique_together = ['team', 'title']

    def __str__(self):
        return self.title


class Homework(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='homework')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='homeworks')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='students')
    description = models.TextField()
    homework_file = models.FileField(upload_to='homeworks', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'team']

    def __str__(self):
        return f"{self.student.user.first_name}-- {self.lesson.title}"

class Date(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='team',null=True,blank=True)

    def __str__(self):
        return str(self.date)

class Davomat(models.Model):
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='teamsa',null=True,blank=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    date = models.ForeignKey(Date,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.student.user.first_name}"



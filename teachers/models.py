from django.db import models
from users.models import Student, Team
from django.db.models import Sum

class Month(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tolov_set')
    month = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f"{self.month} "

class Tolov(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tolovs')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='tolov_sets')
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name="tolov_set")
    oylik = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.student.user.first_name} --> {self.student.user.last_name} ({self.oylik})"

    @classmethod
    def total_oylik_for_month(cls, month_id):
        return cls.objects.filter(month_id=month_id).aggregate(total_oylik=Sum('oylik'))['total_oylik'] or 0

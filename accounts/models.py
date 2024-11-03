from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatar", blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=False)
    gl_unit = models.CharField(max_length=20, choices=[('mg/dl', 'mg/dl'), ('mmol/l', 'mmol/l')], default="mg/dl")
    diabetes_risk = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    def bmi(self):
        if self.height and self.weight:
            return f"{self.weight / (self.height*self.height):.2f}"
        return None

    def get_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
        return age

from django.db import models
from django.contrib.auth.models import User


class MedicalDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description or f'Document {self.id}'

    def file_name(self):
        return self.file.name.split('/')[-1]


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    blood_pressure = models.CharField(max_length=10, blank=True, null=True)
    glucose_level = models.CharField(max_length=10, blank=True, null=True)
    bmi = models.CharField(max_length=10, blank=True, null=True)
    age = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class Symptom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserHealthSurvey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_survey')
    diabetes_status = models.CharField(max_length=20, choices=[
        ('yes', 'Yes'),
        ('no', 'No'),
        ('not_sure', 'Not Sure')
    ])
    blood_sugar_check = models.CharField(max_length=20, choices=[
        ('yes', 'Yes'),
        ('no', 'No'),
        ('sometimes', 'Sometimes')
    ])
    active_lifestyle = models.CharField(max_length=20, choices=[
        ('yes', 'Yes'),
        ('no', 'No'),
        ('sometimes', 'Sometimes')
    ])
    other_illnesses = models.CharField(max_length=5, choices=[
        ('yes', 'Yes'),
        ('no', 'No')
    ])
    diabetes_medication = models.CharField(max_length=5, choices=[
        ('yes', 'Yes'),
        ('no', 'No')
    ])
    family_history = models.CharField(max_length=5, choices=[
        ('yes', 'Yes'),
        ('no', 'No')
    ])
    sugar_intake = models.CharField(max_length=10, choices=[
        ('high', 'High'),
        ('moderate', 'Moderate'),
        ('low', 'Low')
    ])
    symptoms = models.ManyToManyField(Symptom)
    high_blood_pressure = models.CharField(max_length=20, choices=[
        ('yes', 'Yes'),
        ('no', 'No'),
        ('not_sure', 'Not Sure')
    ])
    gestational_diabetes = models.CharField(max_length=20, choices=[
        ('yes', 'Yes'),
        ('no', 'No'),
        ('not_applicable', 'Not Applicable')
    ])

    def __str__(self):
        return f"{self.user.username}'s Health Survey"

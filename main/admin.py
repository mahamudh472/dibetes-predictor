from django.contrib import admin
from .models import MedicalDocument, Entry, UserHealthSurvey


# Register your models here.
@admin.register(MedicalDocument)
class MedicalDocumentAdmin(admin.ModelAdmin):
    list_display = ['description', 'uploaded_at']


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['blood_pressure', 'glucose_level', 'date']


@admin.register(UserHealthSurvey)
class UserHealthSurveyAdmin(admin.ModelAdmin):
    pass


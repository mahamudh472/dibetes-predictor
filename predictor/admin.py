from django.contrib import admin
from .models import DietarySuggestion
# Register your models here.

@admin.register(DietarySuggestion)
class DietarySuggestionAdmin(admin.ModelAdmin):
    pass

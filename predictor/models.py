# models.py
from django.db import models
from django.contrib.auth.models import User
import json


class DietarySuggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suggestions')
    suggestions_json = models.TextField()  # Store suggestions as a JSON string
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save_suggestions(self, suggestions):
        # Convert suggestions to JSON and save
        self.suggestions_json = json.dumps(suggestions)
        self.save()

    def get_suggestions(self):
        # Return suggestions as a Python object
        return json.loads(self.suggestions_json)

    def __str__(self):
        return f"{self.user.username} - Dietary Suggestions"

from django import forms
from .models import MedicalDocument, UserHealthSurvey, Symptom


class MedicalDocumentForm(forms.ModelForm):
    class Meta:
        model = MedicalDocument
        fields = ['file', 'description']


SYMPTOMS_CHOICES = [
    ('frequent_thirst', 'Frequent Thirst'),
    ('frequent_urination', 'Frequent Urination'),
    ('unexplained_weight_loss', 'Unexplained Weight Loss'),
    ('none', 'None'),
]

class UserHealthSurveyForm(forms.ModelForm):
    symptoms = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.all(),  # Fetch all available symptoms from the database
        widget=forms.CheckboxSelectMultiple,  # You can change to SelectMultiple if you prefer
        required=False
    )
    class Meta:
        model = UserHealthSurvey
        fields = [
            'diabetes_status', 'blood_sugar_check', 'active_lifestyle',
            'other_illnesses', 'diabetes_medication', 'family_history',
            'sugar_intake', 'symptoms', 'high_blood_pressure', 'gestational_diabetes'
        ]
        widgets = {
            'diabetes_status': forms.Select(attrs={'class': 'form-select'}),
            'blood_sugar_check': forms.Select(attrs={'class': 'form-select'}),
            'active_lifestyle': forms.Select(attrs={'class': 'form-select'}),
            'other_illnesses': forms.Select(attrs={'class': 'form-select'}),
            'diabetes_medication': forms.Select(attrs={'class': 'form-select'}),
            'family_history': forms.Select(attrs={'class': 'form-select'}),
            'sugar_intake': forms.Select(attrs={'class': 'form-select'}),
            # 'symptoms': forms.SelectMultiple(attrs={'class': 'form-control'}),  # For multiple symptoms selection
            'high_blood_pressure': forms.Select(attrs={'class': 'form-select'}),
            'gestational_diabetes': forms.Select(attrs={'class': 'form-select'}),
        }


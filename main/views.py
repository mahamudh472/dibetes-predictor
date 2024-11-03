from django.utils import timezone

from django.http import JsonResponse
from predictor.views import predict_diabetes
from accounts.models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from .models import MedicalDocument, Entry, UserHealthSurvey
from .forms import MedicalDocumentForm, UserHealthSurveyForm
from datetime import date, datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from predictor.models import DietarySuggestion


def index(request):
    return render(request, "main/index.html")

@login_required(login_url="accounts:login")
def profile(request):
    return render(request, 'main/profile.html')

@login_required(login_url="accounts:login")
def documents(request):
    if request.method == 'POST':
        form = MedicalDocumentForm(request.POST, request.FILES)
        print("working")
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user  # Assign the logged-in user
            document.save()
            return redirect('main:documents')  # Redirect to document list after uploading
        print("form is not valid")
    else:
        form = MedicalDocumentForm()
    document_li = MedicalDocument.objects.filter(user=request.user)

    return render(request, 'main/document_list.html', {'form': form, 'documents': document_li})

@login_required(login_url="accounts:login")
def delete_document(request, file_id):
    file = MedicalDocument.objects.get(id=file_id)
    if file:
        file.delete()
    return redirect("main:documents")

@login_required(login_url="accounts:login")
def calendar_view(request):
    today = date.today()
    entries = Entry.objects.filter(user=request.user, date=today).first()
    return render(request, 'main/calendar.html', {
        'today': today,
        'entries': entries
    })

@login_required(login_url="accounts:login")
def get_entries_by_date(request, selected_date):
    entries = Entry.objects.filter(user=request.user, date=selected_date).first()
    if entries:
        gl = entries.glucose_level
        if request.user.userprofile.gl_unit == "mmol/l":
            gl = float(entries.glucose_level) / 18

        return JsonResponse({'blood_pressure': entries.blood_pressure, 'glucose_level': gl})
    return JsonResponse({'blood_pressure': '', 'glucose_level': ''})

@login_required(login_url="accounts:login")
@csrf_exempt
def save_entry(request, selected_date):
    if request.method == 'POST':
        blood_pressure = request.POST.get('blood_pressure')
        glucose_level = request.POST.get('glucose_level')
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()

        # Check if entry already exists or create a new one
        entry, created = Entry.objects.get_or_create(user=request.user, date=selected_date)

        # Update the entry
        entry.blood_pressure = blood_pressure
        if request.user.userprofile.gl_unit == "mmol/l":
            glucose_level = float(glucose_level)*18
        entry.glucose_level = glucose_level
        entry.save()

        # Call the predict_diabetes function for prediction and updating the status
        request.POST = request.POST.copy()  # Make request.POST mutable
        request.POST['glucose_mmol'] = glucose_level  # Assuming glucose_level is in mmol/L

        # Only call predict_diabetes if selected_date is today
        if selected_date == date.today():
            request.POST = request.POST.copy()  # Make request.POST mutable
            request.POST['glucose_mmol'] = glucose_level  # Assuming glucose_level is in mmol/L

            # Call the prediction function
            predict_diabetes(request)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})


@login_required
def health_survey(request):
    # Try to get the user's existing survey, or create a new one if it doesn't exist
    survey, created = UserHealthSurvey.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        print(request.POST)
        form = UserHealthSurveyForm(request.POST, instance=survey)  # Use the existing instance
        if form.is_valid():
            form.save()  # This will update the existing survey or create a new one if needed
            if survey.diabetes_status == "yes":
                up = request.user.userprofile
                up.status = True
                up.save()
            return redirect('main:index')  # Replace with your redirect logic
    else:
        form = UserHealthSurveyForm(instance=survey)  # Pre-populate the form with existing data

    return render(request, 'main/survey.html', {'form': form})

@login_required(login_url="accounts:login")
def dashboard_view(request):
    # Get current month and year if not provided
    current_date = timezone.now()
    month = int(request.GET.get('month', current_date.month))
    year = int(request.GET.get('year', current_date.year))

    # Filter entries for the logged-in user by selected month and year
    entries = Entry.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    ).order_by('date')

    # Prepare data for Chart.js
    labels = [entry.date.strftime('%Y-%m-%d') for entry in entries]
    bp_data = [entry.blood_pressure.split('/')[-1] for entry in entries]
    gl_data = [entry.glucose_level for entry in entries]

    # Pass the month and year options
    month_range = range(1, 13)
    year_range = range(2020, datetime.now().year + 1)

    context = {
        'labels': labels,
        'bp_data': bp_data,
        'gl_data': gl_data,
        'month': month,
        'year': year,
        'month_range': month_range,
        'year_range': year_range,
    }

    return render(request, 'main/dashboard.html', context)

@login_required(login_url="accounts:login")
def prediction(request):
    return render(request, 'main/prediction.html')

@login_required(login_url="accounts:login")
def dietary_suggestion(request):
    dietary_suggestions = DietarySuggestion.objects.filter(user=request.user).last()

    return render(request, 'main/dietary_suggestion.html', {'suggestion': dietary_suggestions})

@login_required(login_url="accounts:login")
def get_filled_dates(request):
    # Assuming your model has a 'date' field in 'YYYY-MM-DD' format
    user = request.user
    filled_dates = Entry.objects.filter(user=user).values_list('date', flat=True).distinct()
    

    return JsonResponse({'filled_dates': list(filled_dates)})

def user_manual(request):
    return render(request, 'main/user_manual.html')

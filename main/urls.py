from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path('', views.index, name="index"),
    path('profile/', views.profile, name="profile"),
    path('documents/', views.documents, name="documents"),
    path('delete_document/<int:file_id>', views.delete_document, name="delete_file"),
    path('health_survey', views.health_survey, name="health_servey"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('prediction/', views.prediction, name="prediction"),
    path('dietary_suggestion/', views.dietary_suggestion, name="dietary_suggestion"),
    # Calendar view showing today's data
    path('calendar/', views.calendar_view, name='calendar_view'),

    # Fetch entries for a specific date
    path('entries/<str:selected_date>/', views.get_entries_by_date, name='get_entries_by_date'),

    # Save or update entry for a specific date
    path('save-entry/<str:selected_date>/', views.save_entry, name='save_entry'),
    path('filled-dates/', views.get_filled_dates, name="filled_dates"),
    path('usermanual/', views.user_manual, name="user_manual")
]

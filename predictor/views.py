import joblib
import pandas as pd
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from accounts.models import UserProfile
from .models import DietarySuggestion

# Load the trained model and scaler
model = joblib.load('saved_model/model.pkl')
scaler = joblib.load('saved_model/scaler.pkl')


@csrf_exempt
def predict_diabetes(request):
    if request.method == 'POST':
        try:
            # Get user profile for age and BMI calculation
            user_profile = UserProfile.objects.get(user=request.user)

            # Access BMI and age from the profile

            bmi = float(user_profile.bmi())
            age = user_profile.get_age()  # Assuming this is a method for calculating age

            # Get blood pressure and glucose level from the form
            blood_pressure = float(request.POST.get('blood_pressure').split('/')[-1])
            glucose_level = float(request.POST.get('glucose_level'))
            # Convert glucose level if needed (based on unit in user profile)
            if user_profile.gl_unit == 'mmol/l':
                glucose_input = glucose_level * 18  # Convert mmol/L to mg/dL
            else:
                glucose_input = glucose_level
            # Prepare input data as a DataFrame with the correct feature names
            input_data = pd.DataFrame([[glucose_input, blood_pressure, bmi, age]],
                                      columns=['Glucose', 'BloodPressure', 'BMI', 'Age'])

            # Scale the input values using the saved scaler
            input_data_scaled = scaler.transform(input_data)
            # Predict using the saved model
            prediction = model.predict(input_data_scaled)
            # Get the probability of having diabetes
            diabetes_risk = model.predict_proba(input_data_scaled)[0][1]  # Probability of positive class (diabetes)
            user_profile.diabetes_risk = f"{diabetes_risk * 100:.2f}%"
            user_profile.save()
            user_suggestions_view(request, diabetes_risk*100)
            # Update the user profile with diabetes status based on prediction
            if prediction[0] == 1:
                user_profile.status = True  # Diabetes detected
            

            # Save the updated status in the profile
            user_profile.save()

            return JsonResponse({'status': 'success', 'diabetes_status': user_profile.status})

        except UserProfile.DoesNotExist:
            return JsonResponse({'status': 'failed', 'error': 'UserProfile not found'})

        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            return JsonResponse({'status': 'failed', 'error': str(e)})

    return JsonResponse({'status': 'failed', 'error': 'Invalid request method'})


def get_dietary_suggestions(risk_percentage):
    if risk_percentage < 30:
        return {
            "Overview": "You have a low risk of diabetes. Maintain a balanced diet to promote overall health.",
            "Suggestions": [
                {
                    "Meal_Type": "Breakfast",
                    "Ideas": [
                        "Oatmeal topped with fresh berries and a sprinkle of cinnamon.",
                        "Greek yogurt with honey and mixed nuts.",
                        "Smoothie made with spinach, banana, and almond milk."
                    ],
                    "Portion_Size": "Keep portions moderate, especially with grains and nuts."
                },
                {
                    "Meal_Type": "Lunch",
                    "Ideas": [
                        "Quinoa salad with chickpeas, cucumber, and olive oil dressing.",
                        "Grilled chicken wrap with lots of veggies and a whole grain tortilla.",
                        "Vegetable stir-fry with tofu and brown rice."
                    ],
                    "Portion_Size": "Aim for a balanced plate: 1/2 veggies, 1/4 protein, 1/4 whole grains."
                },
                {
                    "Meal_Type": "Dinner",
                    "Ideas": [
                        "Baked salmon with a side of steamed broccoli and sweet potatoes.",
                        "Whole wheat pasta with marinara sauce and a mixed green salad.",
                        "Stuffed bell peppers with ground turkey and brown rice."
                    ],
                    "Portion_Size": "Include a variety of colors on your plate for optimal nutrition."
                },
                {
                    "Snacks": [
                        "Fresh fruit like apples or oranges.",
                        "Carrot sticks with hummus.",
                        "A handful of almonds."
                    ]
                }
            ]
        }
    elif risk_percentage < 60:
        return {
            "Overview": "You are at moderate risk for diabetes. Focus on maintaining a balanced diet while limiting "
                        "certain food groups.",
            "Suggestions": [
                {
                    "Meal_Type": "Breakfast",
                    "Ideas": [
                        "Whole grain toast with avocado and a poached egg.",
                        "Smoothie with spinach, protein powder, and a small banana.",
                        "Chia seed pudding topped with berries."
                    ],
                    "Portion_Size": "Limit added sugars and opt for whole grains."
                },
                {
                    "Meal_Type": "Lunch",
                    "Ideas": [
                        "Lentil soup with a side salad dressed with olive oil.",
                        "Grilled vegetable sandwich on whole grain bread.",
                        "Tuna salad served on mixed greens with balsamic vinaigrette."
                    ],
                    "Portion_Size": "Choose lean proteins and high-fiber foods."
                },
                {
                    "Meal_Type": "Dinner",
                    "Ideas": [
                        "Stir-fried shrimp with mixed vegetables and quinoa.",
                        "Baked chicken breast with roasted Brussels sprouts and brown rice.",
                        "Zucchini noodles topped with marinara sauce and turkey meatballs."
                    ],
                    "Portion_Size": "Watch for Portion_Sizes on starchy foods."
                },
                {
                    "Snacks": [
                        "Plain popcorn (air-popped).",
                        "Greek yogurt with a sprinkle of cinnamon.",
                        "Sliced bell peppers with guacamole."
                    ]
                }
            ]
        }
    else:  # High risk
        return {
            "Overview": "You are at high risk for diabetes. A strict dietary regimen is essential for managing your "
                        "health.",
            "Suggestions": [
                {
                    "Meal_Type": "Breakfast",
                    "Ideas": [
                        "Scrambled eggs with spinach and tomatoes.",
                        "Overnight oats made with unsweetened almond milk and chia seeds.",
                        "A smoothie with kale, avocado, and a small portion of low-sugar fruit."
                    ],
                    "Portion_Size": "Keep carbohydrate portions small."
                },
                {
                    "Meal_Type": "Lunch",
                    "Ideas": [
                        "Salad with grilled chicken, assorted greens, nuts, and a vinaigrette.",
                        "Quinoa bowl with black beans, corn, avocado, and a squeeze of lime.",
                        "Broiled fish tacos with cabbage slaw on corn tortillas."
                    ],
                    "Portion_Size": "Focus on non-starchy vegetables and lean proteins."
                },
                {
                    "Meal_Type": "Dinner",
                    "Ideas": [
                        "Grilled turkey burgers wrapped in lettuce leaves with salsa.",
                        "Baked cod with asparagus and a small baked sweet potato.",
                        "Cauliflower rice stir-fry with vegetables and tofu."
                    ],
                    "Portion_Size": "Limit Portion_Sizes of starchy foods; fill up on vegetables."
                },
                {
                    "Snacks": [
                        "Celery sticks with almond butter.",
                        "Cucumber slices with vinegar.",
                        "A small serving of mixed nuts."
                    ]
                }
            ]
        }


def user_suggestions_view(request, risk_percentage):

    # Generate dietary suggestions based on the risk percentage
    suggestions = get_dietary_suggestions(risk_percentage)

    # Get today's date
    today = timezone.now().date()

    # Check if a suggestion already exists for today
    dietary_suggestion, created = DietarySuggestion.objects.get_or_create(
        user=request.user,
        created_at__date=today  # Ensure we're checking against the created_at field
    )

    # Update or create suggestions
    dietary_suggestion.save_suggestions(suggestions)

    # Optionally, you can also update the updated_at field manually if needed
    dietary_suggestion.updated_at = timezone.now()
    dietary_suggestion.save()

    return

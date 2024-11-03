from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate 
from .models import UserProfile, User
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.conf import settings
from .custom_decorators import redirect_if_authenticate
# Create your views here.

@redirect_if_authenticate
def loginView(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            try:
                username = username.split('@')[0]
                user = authenticate(username=username, password=password)
                if not user:
                    raise ValueError
            except:
                messages.error(request, "Authentication error")
                return redirect("accounts:login")
        
        # User authenticated, now send OTP
        otp = send_otp(user.email)
        request.session['otp'] = otp
        request.session['login_user_id'] = user.id

        return redirect('accounts:verify_login_otp')

    return render(request, "accounts/login.html")



def send_otp(email):
    # Generate a 6-digit random OTP
    otp = random.randint(100000, 999999)
    # Send OTP to the user's email
    send_mail(
        'Your OTP for account registration',
        f'Your OTP is {otp}. Please use it to complete your registration.',
        f'{email}',  # Replace with your actual email
        [email],
        fail_silently=False,
    )
    return otp

@redirect_if_authenticate
def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        username = email.split("@")[0]

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("accounts:register")

        if password != password2:
            messages.error(request, "Password not matched")
            return redirect("accounts:register")
        
        # Send OTP and store it in session
        otp = send_otp(email)
        request.session['otp'] = otp
        request.session['user_data'] = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'dob': dob,
            'email': email,
            'password': password,
        }

        # Redirect to OTP verification view
        return redirect('accounts:verify_otp')

    return render(request, "accounts/signup.html")

def logoutView(request):
    logout(request)
    return redirect('accounts:login')

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp')
        user_data = request.session.get('user_data')

        if entered_otp == str(saved_otp):
            # OTP matched, create user and profile
            user = User.objects.create_user(
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data['password']
            )
            user.save()

            userprofile = UserProfile.objects.create(
                user=user,
                gender=user_data['gender'],
                date_of_birth=user_data['dob']
            )
            userprofile.save()

            login(request, user)
            
            return redirect("main:health_servey")
        else:
            messages.error(request, "Invalid OTP")
            return redirect("accounts:verify_otp")

    return render(request, "accounts/verify_otp.html")


def verify_login_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp')
        login_user_id = request.session.get('login_user_id')

        if entered_otp == str(saved_otp):
            # OTP matched, log the user in
            user = User.objects.get(id=login_user_id)
            login(request, user)
            del request.session['otp']
            del request.session['login_user_id']
            return redirect("main:index")
        else:
            messages.error(request, "Invalid OTP")
            return redirect("accounts:verify_login_otp")

    return render(request, "accounts/verify_otp.html")

def resend_otp(request):
    # Check if the session has OTP data for registration or login
    if request.session.get('user_data') or request.session.get('login_user_id'):
        # Generate a new OTP
        new_otp = random.randint(100000, 999999)
        
        # Update OTP in session
        request.session['otp'] = new_otp
        
        # Check if it's for registration or login
        if request.session.get('user_data'):
            user_data = request.session['user_data']
            email = user_data['email']
        elif request.session.get('login_user_id'):
            user = User.objects.get(id=request.session['login_user_id'])
            email = user.email
        
        
        # Send the OTP to the user's email
        subject = "Your OTP Code"
        message = f"Your OTP code is {new_otp}."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

        messages.success(request, "A new OTP has been sent to your email.")
        return redirect(request.META.get('HTTP_REFERER'))  # Redirect back to the OTP page
    else:
        # If no session data, redirect to login or register
        return redirect('accounts:login')


def change_profile_photo(request):
    if request.method == "POST":
        photo = request.FILES['photo']
        userprofile = UserProfile.objects.get(user=request.user)
        userprofile.avatar = photo
        userprofile.save()
    return redirect("main:profile")

def update_profile_info(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.userprofile.gender = request.POST.get('gender')
        user.userprofile.date_of_birth = request.POST.get('dob')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        if height:
            user.userprofile.height = height
        if weight:
            user.userprofile.weight = weight
        user.userprofile.address = request.POST.get('address')
        user.userprofile.phone = request.POST.get('phone')
        user.userprofile.gl_unit = request.POST.get('gl_unit')
        user.save()
        user.userprofile.save()
    return redirect('main:profile')

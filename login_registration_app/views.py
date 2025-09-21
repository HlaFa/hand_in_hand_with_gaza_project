from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from login_registration_app.forms import LoginForm, RegisterForm
from login_registration_app.models import User


def welcome(request):
    return render(request, 'welcome.html')


def about(request):
    return render(request, 'about.html')


#///////////////////////////////////////////login/////////////////////////////////////
def login_template(request):
    return render(request, "login.html", {"form": LoginForm()})


def login_submit(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    request.session['role'] = user.role
                    messages.success(request, f"Welcome back, {user.first_name}!")

                    if user.role == 'donor': 
                        return redirect('donor_app:dashboard')
                    if user.role == 'recipient':
                        return redirect('recipient_app:home')
                          
                else:
                    messages.error(request, "Incorrect password.")
            except User.DoesNotExist:
                messages.error(request, "User does not exist.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


# /////////////////////////////////////////////////////////regiser///////////////////////////////////////
def register_template(request):
    return render(request, "signup.html", {"form": RegisterForm()})


def register_submit(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save() 
            request.session['user_id'] = user.id
            request.session['role'] = user.role
            messages.success(request, f"Welcome {user.first_name}, your account has been created!")
            

            if user.role == 'donor':
                return redirect('donor_app:dashboard')
            if user.role == 'recipient':
                return redirect('recipient_app:home')
           
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "signup.html", {"form": form})
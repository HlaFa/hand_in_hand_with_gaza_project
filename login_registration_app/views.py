
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from login_registration_app.forms import LoginForm, ProfileEditForm, RegisterForm
from login_registration_app.models import User
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

def welcome(request):
    return render(request, 'welcome.html')


def about(request):
    return render(request, 'about.html')


# /////////////////////////////////////////// LOGIN ///////////////////////////////////////
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
                    request.session['first_name'] = user.first_name 
                    messages.success(request, f"Welcome back, {user.first_name}!")

                    role = user.role.lower()
                    if role == 'donor':
                        return redirect('donor_app:dashboard')
                    elif role == 'recipient':
                        return redirect('recipient_app:home')
                    else:
                        messages.error(request, f"Unknown role: {user.role}")
                        return redirect('login_registration_app:login_template')
                else:
                    messages.error(request, "Incorrect password.")
            except User.DoesNotExist:
                messages.error(request, "User does not exist.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})
# /////////////////////////////////////////// REGISTER ///////////////////////////////////////
def register_template(request):
    return render(request, "signup.html", {"form": RegisterForm()})


def register_submit(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            request.session['user_id'] = user.id
            request.session['role'] = user.role
            request.session['first_name'] = user.first_name 
            messages.success(request, f"Welcome {user.first_name}, your account has been created!")

            role = user.role.lower()
            if role == 'donor':
                return redirect('donor_app:dashboard')
            elif role == 'recipient':
                return redirect('recipient_app:home')
            else:
                messages.error(request, f"Unknown role: {user.role}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "signup.html", {"form": form})


# /////////////////////////////////////////// LOGOUT ///////////////////////////////////////
def logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('login_registration_app:login_template')

# /////////////////////////////////////////// Edit Profile ///////////////////////////////////////

def profile_edit(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "message": "You must be logged in."})

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            role = request.session.get("role")
            if role == "donor":
                redirect_url = reverse("donor_app:dashboard")
            else:
                redirect_url = reverse("recipient_app:home")

            if form.has_changed():
                user = form.save()
                request.session['first_name'] = user.first_name

                return JsonResponse({
                    "success": True,
                    "message": "Profile updated successfully.",
                    "redirect_url": redirect_url,
                    "updated_name": user.first_name
                })
            else:
                return JsonResponse({
                    "success": False,
                    "message": "No changes were made.",
                    "redirect_url": redirect_url
                })
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = ProfileEditForm(instance=user)

    return render(request, "profile_edit.html", {"form": form})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from login_registration_app.models import Case, User
from .forms import CaseForm
from .models import *

# Recipient Dashboard (create + list cases)
@login_required
def recipient_dashboard(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login_registration_app:login_template")  # not logged in

    user = User.objects.get(id=user_id)  # ✅ get your custom user
    my_cases = Case.objects.filter(user=user)

    return render(request, "recipient_dashboard.html", {
        "my_cases": my_cases
    })
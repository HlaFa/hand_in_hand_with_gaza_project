from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from login_registration_app.models import Case, User
from login_registration_app.notify_admin import notify_admin_new_case
from .forms import CaseForm
from .models import *

from django.shortcuts import render

def recipient_home(request):
    uid = request.session.get("user_id")
    if not uid or request.session.get("role") != "recipient":
        return redirect("login_registration_app:login_template")

    user = User.objects.get(id=uid)
    if request.method == "POST":
        form = CaseForm(request.POST, request.FILES)
        if form.is_valid():
            case = form.save(user=user) 
            notify_admin_new_case(case) 
            messages.info(request, "Case submitted! Waiting for admin proof approval.")
            return redirect("recipient_app:home")
    else:
        form = CaseForm()

    my_cases = Case.objects.filter(user=user).order_by("-created_at")
    return render(request, "recipient_dashboard.html", {
        "form": form,
        "my_cases": my_cases
    })
 

def case_status(request, case_id):
    try:
        case = Case.objects.get(id=case_id)
        attachments = list(case.case_attachments.values("id", "status"))
        return JsonResponse({
            "status": case.status,
            "attachments": attachments
        })
    except Case.DoesNotExist:
        return JsonResponse({"error": "Case not found"}, status=404)



def delete_case(request, case_id):
    if request.method == "POST":
        case = get_object_or_404(Case, id=case_id)

        if str(case.user_id) != str(request.session.get("user_id")):
            messages.error(request, "You cannot delete this case.")
            return HttpResponseForbidden("You cannot delete this case.")

        if case.status.lower() == "rejected":
            case.delete()
            messages.success(request, "Case deleted successfully.")
        else:
            messages.warning(request, "Only rejected cases can be deleted.")

    return redirect("recipient_app:home")
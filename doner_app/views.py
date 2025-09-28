
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from login_registration_app.models import Case, Adoption, User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def donor_dashboard(request):
    cases = Case.objects.filter(status="approved").order_by("-created_at")
    return render(request, "donor_dashboard.html", {"cases": cases})


def case_detail(request, case_id):
    case = get_object_or_404(Case, id=case_id, status="approved")
    attachments = case.case_attachments.all()
    return render(request, "case_detail.html", {"case": case, "attachments": attachments})


def adopt_case(request, case_id):
    if request.method == "POST":
        case = get_object_or_404(Case, id=case_id, status="approved")
        donor = User.objects.get(id=request.session["user_id"])  
        amount = request.POST.get("amount")

        if not amount or float(amount) <= 0:
            return JsonResponse({"error": "Enter valid amount"}, status=400)

        Adoption.objects.create(
            donor=donor,
            case=case,
            amount=amount
        )

        total = case.adoptions.aggregate(total=Sum("amount"))["total"] or 0

        if total >= case.price:
            case.status = "delivered"
            case.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"case_{case.id}",
            {
                "type": "status.update", 
                "status": case.status,
                "attachments": list(case.case_attachments.values("id", "status"))
            }
        )

        return JsonResponse({
            "success": True,
            "message": "Donation successful!",
            "status": case.status
        })

def my_adoptions(request):
    donor_id = request.session.get("user_id")
    adoptions = Adoption.objects.filter(donor_id=donor_id).select_related("case")

    return render(request, "my_adoptions.html", {"adoptions": adoptions})        
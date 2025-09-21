
from django.shortcuts import render
from django.http import HttpResponse

def donor_dashboard(request):
    return render(request, "donor_dashboard.html")   
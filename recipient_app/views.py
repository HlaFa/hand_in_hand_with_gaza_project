from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def recipient_dashboard(request):
    return render(request,"recipient_dashboard.html")

from django.urls import path
from . import views

app_name = "donor_app"
urlpatterns = [
    path('dashboard', views.donor_dashboard, name='dashboard'),
    ]
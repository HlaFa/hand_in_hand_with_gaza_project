from django.urls import path
from . import views

app_name = "recipient_app"
urlpatterns = [
    path('home', views.recipient_dashboard, name='home'),
    ]
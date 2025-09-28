
from django.urls import path
from . import views

app_name = "recipient_app"

urlpatterns = [
    path("home/", views.recipient_home, name="home"),
    path("case-status/<int:case_id>/", views.case_status, name="case_status"),
    path("case-delete/<int:case_id>/", views.delete_case, name="delete_case"),
]
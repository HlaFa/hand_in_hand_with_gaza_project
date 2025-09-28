from django.urls import path
from . import views

app_name = "donor_app"

urlpatterns = [
    path("dashboard/", views.donor_dashboard, name="dashboard"),
    path('case/<int:case_id>/', views.case_detail, name="case_detail"),
    path('adopt/<int:case_id>/', views.adopt_case, name="adopt_case"),
    path("my-adoptions/", views.my_adoptions, name="my_adoptions"),
]
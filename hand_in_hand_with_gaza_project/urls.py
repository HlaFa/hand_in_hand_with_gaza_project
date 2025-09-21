
from django.urls import path,include
urlpatterns = [
    path('', include('login_registration_app.urls',namespace="login_registration_app"),),
    path('', include('recipient_app.urls',namespace="recipient_app"),),
    path('', include('doner_app.urls',namespace="donor_app"),),
    ]

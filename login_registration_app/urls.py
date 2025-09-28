from django.urls import path
from . import views
app_name = "login_registration_app"
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('about',views.about,name='about'),
    path('accounts/login/', views.login_template, name='login_template'), 
    path('login/submit', views.login_submit, name='login_submit'),
    path('register/', views.register_template, name='register_template'), 
    path('register/submit', views.register_submit, name='register_submit'),
    path('logout/', views.logout, name='logout'),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    ]

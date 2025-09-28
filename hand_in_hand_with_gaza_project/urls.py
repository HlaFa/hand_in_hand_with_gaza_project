
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login_registration_app.urls',namespace="login_registration_app"),),
    path('', include('recipient_app.urls',namespace="recipient_app"),),
    path('', include('doner_app.urls',namespace="donor_app"),),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

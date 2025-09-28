from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/case/<int:case_id>/", consumers.CaseConsumer.as_asgi()),
]
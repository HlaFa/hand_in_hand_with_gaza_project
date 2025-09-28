import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import recipient_app.routing   # 👈 your websocket routes

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hand_in_hand_with_gaza_project.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            recipient_app.routing.websocket_urlpatterns
        )
    ),
})

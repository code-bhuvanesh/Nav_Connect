
import os 
  
import django 
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter 
from channels.routing import ProtocolTypeRouter, URLRouter
from api.routing import ws_urlpatterns

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'navconnect.settings')

asgi_app = get_asgi_application()

application = ProtocolTypeRouter({ 
    'http': asgi_app,
    "websocket": 
            URLRouter(
                ws_urlpatterns
            )
})

app = application
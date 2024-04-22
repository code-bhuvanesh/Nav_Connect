from django.urls import re_path
from .consumers import *

ws_urlpatterns = [
    re_path(r"^ws/buslocation/(?P<busid>\w+)", BusLocationConsumer.as_asgi())
    # re_path(r"^ws/buslocation/", BusLocationConsumer.as_asgi())
]   

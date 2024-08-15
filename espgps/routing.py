from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/device/(?P<device_id>\w+)/$', consumers.DeviceConsumer.as_asgi()),
]
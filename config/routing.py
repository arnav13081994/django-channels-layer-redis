# iot/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/calculate/$", consumers.CalculateSumConsumer.as_asgi()),
    re_path(r"ws/calculate-json/$", consumers.CalculateSumConsumerJSON.as_asgi()),
]

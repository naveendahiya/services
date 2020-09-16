from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url
from service import consumers

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<task_id>[^/]+)/(?P<user_id>[^/]+)$', consumers.ChatConsumer),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
import main_channel.routing

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            main_channel.routing.websocket_urlpatterns
        )
    )
})

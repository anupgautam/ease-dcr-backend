from django.urls import path


from . import consumers

websocket_urlpatterns = [
    path('ws/ac/', consumers.ChatDefaultAsyncConsumer.as_asgi()),
    path('ws/ac/notification/', consumers.ChatNotificationAsyncConsumer.as_asgi()),
    path('ws/ac/<str:group>/', consumers.ChatAsyncConsumer.as_asgi()),

]
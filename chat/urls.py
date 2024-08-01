from rest_framework.routers import DefaultRouter
from django.urls import path

from chat.views import (
    GroupViewSets,
    ChatViewSets,
    GroupMembersMapViewSets,
    GroupMembersViewSets,
    GroupMembersMapAllViewset,
    PushNotificationViewSet,
    GeneralNotificationViewSet,
    get_group_by_user,
    get_my_ws_connection)


routers = DefaultRouter()

routers.register(r'group', GroupViewSets,
                 basename="group")
routers.register(r'chat', ChatViewSets,
                 basename="chat")
routers.register(r'group-member', GroupMembersViewSets,
                 basename="group_member")
routers.register(r'group-member-map', GroupMembersMapViewSets,
                 basename="group_member_map")
routers.register(r'group-members-all', GroupMembersMapAllViewset,
                 basename='group_members_all')
routers.register(r'notification', PushNotificationViewSet,
                 basename="notification")
routers.register(r'general-notification', GeneralNotificationViewSet,
                 basename="general_notification")

urlpatterns = [
    path('user-group/', get_group_by_user, name="user_group"),
    path('user-ws/', get_my_ws_connection, name="user-ws")
]
urlpatterns += routers.urls
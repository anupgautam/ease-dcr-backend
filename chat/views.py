from rest_framework import viewsets, pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action
from django.db.models import Q

from utility.logic import RetrieveLogicID, formdata_application_json, RetrieveLogicUUID

from utility.get_template_data import get_template_data
from Account.models import User
from chat.models import (
    Group, Chat, GroupMembers, GroupMembersMap, PushNotification, GeneralNotification)
from chat.serializers import (
    GroupSerializers,
    ChatSerializers,
    GroupMembersSerializers,
    GroupMembersMapSerializers,
    GroupMembersMapAllSerializers,
    PushNotificationSerializers,
    GeneralNotificationSerializers
)
from .utils import (
    get_group_from_users,
    create_mapped_group_data,
    UserTypeAccessUserTest,
    UserTypeAccessUserList)
from utility.get_user_access import get_user_from_access
from utility.get_uuid import generate_8_digit_uuid
from .constant import WEB_SOCKET_BASE_URL


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """
    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False
    

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Maximum number of items per page
    

class GroupViewSets(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'destroy', 'create'],
        AllowAny: ['retrieve', 'list']
    }

    def create(self, request, *args, **kwargs):
        user = get_user_from_access(request.data.get('user'))
        customer_list = request.data.get('customer')
        customer_list.append(user)
        user_group = get_group_from_users(customer_list)
        if user_group:
            serializer = self.serializer_class(user_group, many=True)
            return Response(
                    data=serializer.data,
                    status=status.HTTP_200_OK)
        else:
            serializer = self.serializer_class(
                            data={'unique_id': generate_8_digit_uuid()})
            if serializer.is_valid():
                serializer.save()

                create_mapped_group_data(
                    customer_list, int(serializer.data.get('id')))
                return Response(
                    data=serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )


class ChatViewSets(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'destroy', 'create'],
        AllowAny: ['retrieve', 'list'],
    }

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # Apply any filtering or sorting you need on the queryset

    #     # Apply pagination
    #     paginator = CustomPagination()
    #     result_page = paginator.paginate_queryset(queryset, self.request)
    #     return result_page

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def get_my_chat(self, request):
        user_list = request.data.get('user_list')
        data_length = request.data.get('data_length')
        initial = (int(data_length)-1)*10
        final = int(data_length)*10
        chat_data = Chat.objects.filter(
            initiator__in=user_list,
            receiver__in=user_list
        ).order_by('-created_date')[initial:final]
        serializer = self.serializer_class(chat_data, many=True)
        return Response(
            data={'data': serializer.data},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def get_my_users(self, request):
        current_user = request.data.get('user')
        chat_list = Chat.objects.filter(
            Q(initiator=current_user)|
            Q(receiver=current_user)
        )
        receiver_list = [int(i.receiver.id) for i in chat_list]
        initiator_list = [int(i.initiator.id) for i in chat_list]
        final_list = list(set(receiver_list+initiator_list))
        data = UserTypeAccessUserList(UserTypeAccessUserTest, final_list).get_user_obj()
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class GroupMembersViewSets(viewsets.ModelViewSet):
    queryset = GroupMembers.objects.all()
    serializer_class = GroupMembersSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'destroy', 'create'],
        AllowAny: ['retrieve', 'list']
    }

    
class GroupMembersMapViewSets(viewsets.ModelViewSet):
    queryset = GroupMembersMap.objects.all()
    serializer_class = GroupMembersMapSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'destroy', 'create'],
        AllowAny: ['retrieve', 'list']
    }


class PushNotificationViewSet(viewsets.ModelViewSet):
    queryset = PushNotification.objects.all()
    serializer_class = PushNotificationSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'destroy', 'create'],
        AllowAny: ['retrieve', 'list']
    }


GROUP_MEMBERS_ALL = [
            {
                'model': GroupMembers,
                'mapped_model': GroupMembersMap,
                'fk_original': 'group_id',
                'fk_map': "group_members_id",
                'serializer': GroupMembersSerializers,
                'mapped_serializer': GroupMembersMapSerializers,
                'model_field_name': 'group_members'
              },
]


class GroupMembersMapAllViewset(viewsets.ViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    serializer_class = GroupMembersMapAllSerializers
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
      AllowAny: ['update', 'partial_update', 'destroy', 'create', 'retrieve', 'list'],
        # IsAdminUser: ['update', 'partial_update', 'destroy', 'create'],
        # AllowAny: ['retrieve', 'list']
    }

    def retrieve(self, request, pk=None):
        chat_data = get_template_data(
            Group,
            GroupSerializers,
            GROUP_MEMBERS_ALL
        )
        data = RetrieveLogicID(chat_data, pk).retrieve()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_404_NOT_FOUND)
 
    def create(self, request):
        serializer = self.serializer_class(
                        data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        context = request.data.get('context')
        data = formdata_application_json(request.data)
        
        serializer = self.serializer_class(
            instance = Group.objects.get(id=pk),
            data=request.data,
            partial=True,
            context=data.get('context'))
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        id = request.data.get('id')
        serializer = self.serializer_class(
            instance = Group.objects.get(id=id),
            data=request.data)
        if serializer.is_valid():
            deleted_return = serializer.delete(request.data)
            serializer1 = self.serializer_class(data=deleted_return)
            if serializer1.is_valid():
                return Response(
                    data=serializer1.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data=serializer1.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class GeneralNotificationViewSet(viewsets.ModelViewSet):
    queryset = GeneralNotification.objects.order_by('-created_date')
    serializer_class = GeneralNotificationSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id',
        'general_notification_sender',
        'general_notification_receiver',
        'is_read']
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'destroy', 'create'],
        AllowAny: ['retrieve', 'list']
    }

        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_group_by_user(request):
    if request.data.get('access'):
            id = get_user_from_access(request.data.get('access'))
    else:
        id = request.data.get('id')
    group_members = GroupMembers.objects.filter(user__id=id)
    if group_members.count()>0:
        group_members_ids = [i.id for i in group_members]
        group_members_map = GroupMembersMap.objects.filter(group_members_id__id__in=group_members_ids)
        group_members_map_id = [i.group_id.id for i in group_members_map]
        groups = Group.objects.filter(id__in=group_members_map_id)
        group_unique_id = [i.unique_id for i in groups]
        group_urls = [f'{WEB_SOCKET_BASE_URL}/ws/ac/'+i+"/" for i in group_unique_id]
        return Response(
            data={'data': group_urls},
            status=status.HTTP_200_OK)
    return Response(
        data={'data': []},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_my_ws_connection(request):
    if request.data.get('access'):
        id = get_user_from_access(request.data.get('access'))
    else:
        id = request.data.get('id')
    group_member = GroupMembers.objects.filter(user__id=id)
    if group_member.count()>0:
        if group_member[0].unique_id:
            data = [f'{WEB_SOCKET_BASE_URL}/ws/ac/'+group_member[0].unique_id+"/"]
            return Response(
                    data={'data': data},
                    status=status.HTTP_200_OK)
        else:
            unique_id = generate_8_digit_uuid()
            GroupMembers.objects.filter(
                user__id=id).update(
                unique_id=unique_id)
            data = [f'{WEB_SOCKET_BASE_URL}/ws/ac/'+unique_id+"/"]
            return Response(
                data={'data': data},
                status=status.HTTP_200_OK
        )
    else:
        GroupMembers.objects.create(
            user=User.objects.get(id=id),
            unique_id=generate_8_digit_uuid()
        )
        group_member = GroupMembers.objects.filter(user__id=id)
        data = [f'{WEB_SOCKET_BASE_URL}/ws/ac/'+group_member[0].unique_id+"/"]
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


        


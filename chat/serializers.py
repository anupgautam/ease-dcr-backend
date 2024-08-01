from rest_framework import serializers

from .constant import BASE_URL
from utility.logic import (CreateLogicID,
                           UpdateLogicID,
                           DeleteLogicID,
                           CreateArrayInsideDictionaryWithQuerySet,
                           CreateArrayInsideDictionaryWithoutQuerySet)
from chat.models import (
    Group, Chat, GroupMembers, GroupMembersMap, PushNotification,GeneralNotification)


class GroupSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Group
        fields = "__all__"


class ChatSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Chat
        fields = "__all__"


class GroupMembersSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = GroupMembers
        fields = "__all__"

    
class GroupMembersMapSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = GroupMembersMap
        fields = "__all__"


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

class GroupMembersMapAllSerializers(serializers.Serializer):
    id = serializers.UUIDField(allow_null=True, required=False)
    unique_id = serializers.CharField(
        allow_null=True,
        allow_blank=True,
        required=False,
        read_only=True)
    group_name = serializers.CharField(
        allow_null=True,
        allow_blank=True,
        required=False)
    group_members = GroupMembersSerializers(
            allow_null=True,
            required=False,
            many=True)

    class Meta:
        update_methods = ['PUT', 'PATCH']

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        original_model = Group
        create_array = CreateArrayInsideDictionaryWithQuerySet
        CreateLogicID(
            GROUP_MEMBERS_ALL,
            original_model,
            validated_data,
            create_array).create()
        original_data = CreateLogicID(
            GROUP_MEMBERS_ALL,
            original_model,
            validated_data,
            create_array).create_return()
        return original_data

    def update(self, instance, validated_data):
        original_model = Group
        create_array = CreateArrayInsideDictionaryWithQuerySet  
        UpdateLogicID(
            GROUP_MEMBERS_ALL,
            original_model,
            validated_data,
            instance,
            self.context,
            create_array
        ).update()
        original_data = UpdateLogicID(
            GROUP_MEMBERS_ALL,
            original_model,
            validated_data,
            instance,
            self.context,
            create_array
        ).update_return()
        return original_data

    def delete(self, request, *args, **kwargs):
        original_model = Group
        create_array = CreateArrayInsideDictionaryWithQuerySet
        DeleteLogicID(
            GROUP_MEMBERS_ALL,
            original_model,
            request,
            create_array
        ).delete()
        original_data = DeleteLogicID(
            GROUP_MEMBERS_ALL,
            original_model,
            request,
            create_array
        ).delete_return()
        return original_data
    

class PushNotificationSerializers(serializers.ModelSerializer):

    class Meta:
        model = PushNotification
        fields = "__all__"


class GeneralNotificationSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = GeneralNotification
        fields = "__all__"


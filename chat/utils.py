from abc import ABC, abstractmethod

from chat.models import GroupMembers, GroupMembersMap, Group
from utility.array_to_dict import array_of_dict_id, array_of_dict_group_id
from Account.models import User
from chat.models import Chat, PushNotification
from channels.db import database_sync_to_async
from DCRUser.models import CompanyUserRole
from Account.models import User
from DCRUser.serializers import (
    CompanyUserRoleSerializers
)
from Account.serializers import UserSerializers


def get_group_from_users(users_id: list):
    group_member_id = GroupMembers.objects.filter(user__id__in=users_id)
    group_member_map_id = GroupMembersMap.objects.filter(
        group_members_id__in=group_member_id)
    return_dict = array_of_dict_group_id(group_member_map_id)
    for key, value in return_dict.items():
        if value == 2:
            return Group.objects.filter(
                id=key)
        else:
            return False
        

def create_mapped_group_data(users_id: list, group_id: int):
    groups_id = []
    for i in users_id:
        if GroupMembers.objects.filter(user__id=i).count()>0:
            groups_id.append(GroupMembers.objects.get(user__id=i).id)
        else:
            group = GroupMembers(user=User.objects.get(id=i))
            group.save()
            groups_id.append(group.id)
    group_members = []
    for i in groups_id:
        group_member = GroupMembers.objects.get(id=i)
        groupies = Group.objects.get(id=group_id)
        group_members.append({
            'group_members_id': group_member,
            'group_id': groupies
        }) 
    group_member_map_instances = [GroupMembersMap(**data) for data in group_members]
    GroupMembersMap.objects.bulk_create(group_member_map_instances)


@database_sync_to_async
def get_initiator_count(initiator_id):
    return User.objects.filter(id=initiator_id).count()


@database_sync_to_async
def get_receiver_count(receiver_id):
    return User.objects.filter(id=receiver_id).count()


@database_sync_to_async
def add_data_without_group(payload):
    if Chat.objects.filter(unique_id=payload['unique_id']).count() == 0:
        Chat.objects.create(
            content=payload['message'],
            initiator=User.objects.get(id=payload['initiator']),
            receiver=User.objects.get(id=payload['receiver']),
            unique_id=payload['unique_id']
        )

@database_sync_to_async
def get_push_notification_data(notification_id):
    return PushNotification.objects.get(id=notification_id)


class UserTypeAccessUserTest:

    def __init__(self, data, role) -> None:
        self.data = int(data)
        super().__init__()

    def test_mpo(self):
        if CompanyUserRole.objects.filter(user_name__id=self.data,
                                          role_name__role_name__role_name="mpo"
                                          ).count()>0:
            return True
        else:
            return False
        
    def test_asm(self):
        if CompanyUserRole.objects.filter(user_name__id=self.data,
                                          role_name__role_name__role_name="asm"
                                          ).count()>0:
            return True
        else:
            return False
    
    def test_rsm(self):
        if CompanyUserRole.objects.filter(user_name__id=self.data,
                                          role_name__role_name__role_name="rsm",
                                          ).count()>0:
            return True
        else:
            return False
    
    def test_dsm(self):
        if CompanyUserRole.objects.filter(user_name__id=self.data,
                                          role_name__role_name__role_name="dsm"
                                          ).count()>0:
            return True
        else:
            return False
        
    def test_gm(self):
        if CompanyUserRole.objects.filter(user_name__id=self.data,
                                          role_name__role_name__role_name="gm"
                                          ).count()>0:
            return True
        else:
            return False
        
    def test_ch(self):
        if CompanyUserRole.objects.filter(user_name__id=self.data,
                                          role_name__role_name__role_name="ch"
                                          ).count()>0:
            return True
        else:
            return False
        
    def test_admin(self):
        if User.objects.filter(
            id=self.data, is_admin=True).count()>0:
            return True
        else:
            return False
        

class UserTypeAccess(ABC):

    @abstractmethod
    def get_user_obj():
        pass


class UserTypeAccessUserList(UserTypeAccess):

    def __init__(self, user_type_test, user_list) -> None:
        self.user_list = user_list
        self.user_type_test = user_type_test
        super().__init__()

    def update_obj(self, data, key, state_variable):
        state_variable[key] = [data]

    def append_update_obj(self, data, key,  state_variable):
        state_variable[key].append(data)

    def update_obj_key(self, key, data, return_obj):
        if return_obj.get(key):
            self.append_update_obj(data, key, return_obj)
        else:
            self.update_obj(data, key, return_obj)

    def create_rolewise_list(self):
        user_obj_return = {}
        for i in self.user_list:
            if self.user_type_test(i).test_mpo():
                # self.user_obj_return['customer'] = self.update_obj_key('customer', i, user_obj_return)
                self.update_obj_key('mpo', i, user_obj_return)

            elif self.user_type_test(i).test_asm():
                # self.user_obj_return['event'] = self.update_obj_key('event', i)
                self.update_obj_key('asm', i, user_obj_return)

            elif self.user_type_test(i).test_rsm():
                # self.user_obj_return['picnic'] = self.update_obj_key('picnic', i)
                self.update_obj_key('rsm', i, user_obj_return)

            elif self.user_type_test(i).test_dsm():
                # self.user_obj_return['hotel'] = self.update_obj_key('hotel', i)
                self.update_obj_key('dsm', i, user_obj_return)

            elif self.user_type_test(i).test_gm():
                # self.user_obj_return['holiday'] = self.update_obj_key('holiday', i)
                self.update_obj_key('gm', i, user_obj_return)

            elif self.user_type_test(i).test_ch():
                # self.user_obj_return['helicopter'] = self.update_obj_key('helicopter', i)
                self.update_obj_key('ch', i, user_obj_return)

            elif self.user_type_test(i).test_admin():
                # self.user_obj_return['admin'] = self.update_obj_key('admin', i)
                self.update_obj_key('admin', i, user_obj_return)

            else:
                pass
        return user_obj_return

    def get_user_obj(self):
        user_obj_return = self.create_rolewise_list()
        service_array = list(user_obj_return.keys())
        copied_obj = user_obj_return.copy()
        for i in service_array:
            if i == "mpo":
                user_obj_return[i] = CompanyUserRoleSerializers(
                    CompanyUserRole.objects.filter(
                    user_name__id__in=copied_obj[i]), many=True
                ).data
            
            elif i == "asm":
                user_obj_return[i] = CompanyUserRoleSerializers(
                    CompanyUserRole.objects.filter(
                    user_name__id__in=copied_obj[i]), many=True
                ).data

            elif i == "rsm":
                user_obj_return[i] = CompanyUserRoleSerializers(
                    CompanyUserRole.objects.filter(
                    user_name__id__in=copied_obj[i]), many=True
                ).data

            elif i == "dsm":
                user_obj_return[i] = CompanyUserRoleSerializers(
                    CompanyUserRole.objects.filter(
                    user_name__id__in=copied_obj[i]), many=True
                ).data

            elif i == "gm":
                user_obj_return[i] = CompanyUserRoleSerializers(
                    CompanyUserRole.objects.filter(
                    user_name__id__in=copied_obj[i]), many=True
                ).data

            elif i == "ch":
                user_obj_return[i] = CompanyUserRoleSerializers(
                    CompanyUserRole.objects.filter(
                    user_name__id__in=copied_obj[i]), many=True
                ).data

            elif i == "admin":
                user_obj_return[i] = UserSerializers(
                    User.objects.filter(
                    id__in=copied_obj[i]), many=True
                ).data

            else:
                pass

        return user_obj_return
        



    





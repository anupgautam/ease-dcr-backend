from django.db import models

from Account.models import User


# Create your models here.
class TimeStampedModels(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CreateUpdateModels(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='%(class)s_creator_name',
                                   blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='%(class)s_updater_name',
                                   blank=True, null=True)

    class Meta:
        abstract = True


class Group(TimeStampedModels, CreateUpdateModels):
    group_name = models.CharField(max_length=100, null=True, blank=True)
    unique_id = models.CharField(max_length=65, null=True, blank=True)


class Chat(TimeStampedModels):
    content = models.TextField(null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE,
        null=True, blank=True
    )
    initiator = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='%(class)s_initiator',
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='%(class)s_receiver',
    )
    unique_id = models.CharField(max_length=65, null=True, blank=True, unique=True)


class GroupMembers(TimeStampedModels, CreateUpdateModels):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True)
    unique_id = models.CharField(
        null=True, blank=True, max_length=32)


class GroupMembersMap(TimeStampedModels, CreateUpdateModels):
    group_members_id = models.ForeignKey(
        GroupMembers,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    group_id = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True, blank=True
    )


class PushNotification(TimeStampedModels, CreateUpdateModels):
    push_notification_title = models.CharField(null=True, blank=True, max_length=100)
    push_notification_description = models.TextField(null=True, blank=True)
    push_notification_image = models.ImageField(null=True, blank=True)
    push_notification_url = models.CharField(null=True, blank=True, max_length=100)


class GeneralNotification(TimeStampedModels):
    general_notification_title = models.CharField(null=True, blank=True, max_length=100)
    general_notification_description = models.TextField(null=True, blank=True)
    general_notification_image = models.ImageField(null=True, blank=True)
    general_notification_url = models.CharField(null=True, blank=True, max_length=100)
    general_notification_sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='%(class)s_notification_sender',)
    general_notification_receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='%(class)s_notification_receiver',
    )
    is_read = models.BooleanField(null=False, blank=False, default=False)
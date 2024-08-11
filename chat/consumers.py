import json

from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer

from .utils import (
    get_initiator_count, get_receiver_count, add_data_without_group,
    get_push_notification_data)


class ChatAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.channel_layer.group_add(
            self.scope['url_route']['kwargs']['group'],
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):

        await self.channel_layer.group_send(
            self.scope['url_route']['kwargs']['group'],
            {
                'type': 'handle.message',
                'message': event['text']
            }
        )

    async def handle_message(self, event):
        data = json.loads(event['message'])
        if data.get('default'):
            await self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({'data': "Default Connection!!!!"}),
                })
        else:
            if data['type'] == "chat":
                if data['is_group']:
                    await self.send({
                        'type': 'websocket.send',
                        'text': json.dumps({'data': "Group Work Left!!!!"}),
                    })
                else:
                    initiator_count = await get_initiator_count(data['initiator'])
                    receiver_count = await get_receiver_count(data['receiver'])

                    if (initiator_count>0 and receiver_count>0):
                        await add_data_without_group(data)
                        await self.send({
                                'type': 'websocket.send',
                                'text': json.dumps(event),
                                    })
                    else:
                        await self.send({
                                'type': 'websocket.send',
                                'text': json.dumps({'data': "User not present in database!!!!"}),
                                    })
            elif data['type'] == "notifications":
                await self.send({
                       'type': 'websocket.send',
                       'text': json.dumps(event), 
                    })
        await self.send({
            'type': 'websocket.send',
            'text': event['message'],
        })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            'events',
            self.channel_name
        )
        raise StopConsumer
    

class ChatDefaultAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        await self.channel_layer.send(
            self.channel_name,
            {
                'type': 'handle.message',
                'message': event['text']
            }
        )

    async def handle_message(self, event):
        user_id = json.loads(event['message'])['user']
        if user_id != 0 or user_id != '0':
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({ 'data': 'You can communicate through this channel!!!!!'}),
            })
        else:
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({'data': 'Communication not possible!!!!!'}),
            })


    async def websocket_disconnect(self, event):
        raise StopConsumer
    

class ChatNotificationAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.channel_layer.group_add("notification_group", self.channel_name)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        await self.channel_layer.group_send(
            "notification_group",
            {
                'type': 'handle.message',
                'message': event['text']
            }
        )

    async def handle_message(self, event):
        if event['message'] is not None:
            data = json.loads(event['message'])
        else:
            data = None
        if data['default']:
            await self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({'data': "Default Connection!!!!"}),
                })
        else:
            if int(data['initiator']) != 0:
                notification = await get_push_notification_data(data['message'])
                sending_data = {
                    'title': notification.push_notification_title,
                    'description': notification.push_notification_description,
                    'image': str(notification.push_notification_image),
                    'url': notification.push_notification_url
                }
                await self.send({
                    'type': 'websocket.send',
                    'text': json.dumps(sending_data)
                })
            else:
                await self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({
                    'data': 'Only Admin can send the push notification'
                })
            })

        if event['message'] is not None:
            data = json.loads(event['message'])
        else:
            data = None
        if data['default']:
            await self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({'data': "Default Connection!!!!"}),
                })
        else:
            if int(data['initiator']) != 0:
                notification = await get_push_notification_data(data['message'])
                sending_data = {
                    'title': notification.push_notification_title,
                    'description': notification.push_notification_description,
                    'image': str(notification.push_notification_image),
                    'url': notification.push_notification_url
                }
                await self.send({
                    'type': 'websocket.send',
                    'text': json.dumps(sending_data)
                })
            else:
                await self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({
                    'data': 'Only Admin can send the push notification'
                })
            })

    async def websocket_disconnect(self, event):
        raise StopConsumer
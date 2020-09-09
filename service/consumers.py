from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from service.models import User
from service.models import Message, Task


class ChatConsumer(WebsocketConsumer):
    def connect(self, data):
        self.room_name = self.scope['url_route']['kwargs']['task_id']
        self.task_id = int(self.room_name)
        self.room_group_name = 'task_%s' % self.room_name

        #checking whether the user is allowed to chat in this room or not
        task = Task.objects.get(pk=self.task_id)
        taskCreater = task.creater
        worker = task.selected

        #current user info
        user_id = data['current_user_id']

        self.access = [taskCreater, worker]
        if user_id in access:
            async_to_sync(self.channel_layer.group_add)(self.room_group_name,
                                                        self.channel_name)
            self.accept()
        else:
            print('this user is not allowed to join this chat')

    def init_chat(self, data):
        user_id = data['user_id']
        user = User.objects.get(pk = user_id)
        content = {
               'command': 'init_chat',
        }
        if user_id in self.accept:
            if not user:
                content['error'] = 'sorry, Your request is not processed right now. Please try again later!'
                self.send_message(content)
        else:
            self.disconnect('Sorry, this user is not allowed to acces this chat')

    def fetch_messages(self, data):
        task = none
        try:
            task = Issue.objects.get(pk=self.task_id)
        except Task.DoesNotExist:
            self.disconnect('Task does not exist')

        messages = task.task_chat.all()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }

        user = data['user_id']
        if user in self.accept:
            self.send_message(content)
        else:
            self.disconnect('Sorry, this user is not allowed to acces this chat')



    def new_message(self, data):
        text = data['text']
        task = Task.objects.get(pk=self.task_id)
        creater_user = User.objects.get(pk = data['user_id'])

       if data['user_id'] in self.accept:
            message = Message.objects.create(creater=creater_user,message=text,task=task)
            content = {
               'command': 'new_message',
                'message': self.message_to_json(message)
            }
            self.send_chat_message(content)
        else:
            self.disconnect('Sorry, this user is not allowed to acces this chat')



    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': str(message.id),
            'creater': message.creater.username,
            'content': message.message,
            'created_at': str(message.timestamp)
        }

    commands = {
        'init_chat': init_chat,
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def disconnect(self, close_code):
        self.send(json.dumps({'end_message': close_code}))
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name,
                                                        self.channel_name)
        self.close()

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'chat_message',
            'message': message
        })

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

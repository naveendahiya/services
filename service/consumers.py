from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from service.models import User
from service.models import Message

class ChatConsumer(WebsocketConsumer):

    def init_chat(self, data):
        username = data['username']
        user = User.objects.get(username = username)
        content = {
            'command': 'init_chat',
        }
        if not user:
            content['error'] = 'sorry, Your request is not processed right now. Please try again later!'
            self.send_message(content)
        
    def fetch_messages(self, data):
        messages = Message.last_50_messages()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        creater = data['from']
        text = data['text']
        creater_user = User.objects.get(username = creater)
        message = Message.objects.create(creater = creater_user, message = text)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return{
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

    def connect(self):
        self.room_name = 'room'
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    def chat_message(self, event):
        message = event['message']
        self.send(text_data = json.dumps(message))
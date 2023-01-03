from channels.generic.websocket import AsyncWebSocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import ChatRoom,ChatMessage

class ChatConsumer(AsyncWebSocketConsumer):
    async def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name='char%s' % self.room_name
        
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        
        await self.accept()
        
        
        
    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.channel_layer,
            self.room_group_name,
        )
        
    ##To handle reciving of message via socket sent from frontend
    
    async def receive(self, message_data):
        data= json.loads(message_data)
        message=data['message']
        username=data['username']
        room=data['room']
        
        
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat_message',
                'message':message,
                'username':username,
                'room':room
            }
        )
        #to save the recieved message into database
        await self.save_messages(username,room,message)
     
     #message sending back to client   
    async def chat_message(self, event):
        message= event['message']
        username=event['username']
        room=event['room']
        
        await self.send(message_data=json.dumps({
                'message':message,
                'username':username,
                'room':room
            
        }))
        
    @sync_to_async    
    def save_messages(Self,username,room,message):
        user=User.objects.get(username=username)
        room=ChatRoom.objects.get(slug=room)
        
        ChatMessage.objects.create(user=user,room=room,message_content=message)
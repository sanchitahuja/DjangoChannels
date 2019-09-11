import json
import asyncio
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import time
from .myAlgo import Algorithm
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'myroom'
        self.room_group_name = 'algo_group'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print("Connected")
        self.accept()
        algorithm=Algorithm()
        while True:
            print("Sent")
            time.sleep(5)
            self.send(text_data=json.dumps({"key":algorithm.returnData()}))


    def disconnect(self, close_code):
        # Leave room group
        print("DisConnected")
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("received")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


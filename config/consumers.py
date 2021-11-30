# iot/consumers.py

import json
from decimal import Decimal

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer


class CalculateSumConsumer(WebsocketConsumer):
    # by default WebsocketConsumer will add every new channel to every group
    # in the groups Iterable and remove it on disconnect
    groups = ["IOT_CalculateSumConsumer"]

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        num_1 = text_data_json["num_1"]
        num_2 = text_data_json["num_2"]
        result = Decimal(num_1) + Decimal(num_2)
        result = float(result)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            # self.group_name,
            self.groups[0],
            {
                "type": "group.sum.message",
                "message": {"result": result, "num_1": num_1, "num_2": num_2},
            },
        )

    # Receive message from room group of type "group.sum.message"
    def group_sum_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))


class CalculateSumConsumerJSON(JsonWebsocketConsumer):
    # by default WebsocketConsumer will add every new channel to every group
    # in the groups Iterable and remove it on disconnect
    groups = ["IOT_CalculateJSONSumConsumer"]

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    # Receive message from WebSocket
    def receive_json(self, content):

        num_1 = content["num_1"]
        num_2 = content["num_2"]
        result = Decimal(num_1) + Decimal(num_2)
        result = float(result)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            # self.group_name,
            self.groups[0],
            {
                "type": "group.sum.message",
                "message": {"result": result, "num_1": num_1, "num_2": num_2},
            },
        )

    # Receive message from room group of type "group.sum.message"
    def group_sum_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send_json(content={"message": message})

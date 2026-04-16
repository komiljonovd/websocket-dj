from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import News
import json


class NewsConsumer(WebsocketConsumer):

    def connect(self):
        self.group_name = "news"

        self.channel_layer = get_channel_layer()

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()


        news = News.objects.all().values(
            'id','title','short_description','description','created_at'
        )

        data = list(news)

        for item in data:
            item['created_at'] = item['created_at'].isoformat()

        self.send(text_data=json.dumps({
            "event": "init",
            "data": data
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def new_news(self, event):
        self.send(text_data=json.dumps({
            "event": "new_news",
            "data": event["document"]
        }))

    def update_news(self, event):
        self.send(text_data=json.dumps({
            "event": "update_news",
            "data": event["document"]
        }))

    def delete_news(self, event):
        self.send(text_data=json.dumps({
            "event": "delete_news",
            "data": {"id": event["news_id"]}
        }))
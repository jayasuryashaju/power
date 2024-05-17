from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class ImportProgressConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            "import_progress",
            self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "import_progress",
            self.channel_name
        )

    def send_progress(self, event):
        self.send(text_data=json.dumps(event))

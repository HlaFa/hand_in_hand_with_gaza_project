import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CaseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.case_id = self.scope["url_route"]["kwargs"]["case_id"]
        self.group_name = f"case_{self.case_id}"

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from group
    async def case_status(self, event):
        await self.send(text_data=json.dumps({
            "status": event["status"]
        }))

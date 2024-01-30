import json
from django.contrib.auth import get_user_model

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .utils import *

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = await get_user_from_cookie(self)
        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        room = await get_room(room_name)
        if room is None:
            await self.close()

        self.scope["user"] = user
        self.scope["room"] = room
        self.room_name = f"{room_name}"
        self.room_group_name = f"chat_{self.room_name}"
        # 그룹 입장
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        """
        사용자와 WebSocket 연결이 끊겼을 때 호출
        """

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        room = self.scope["room"]
        user = self.scope["user"]
        message = text_data_json["message"]
        chat_message = await save_message(room, user, message)

        # #  최근메세지 저장
        # update_room_async = database_sync_to_async(
        #     lambda: setattr(room, "lastest_text", message)
        # )
        # await update_room_async()
        # save_room_async = database_sync_to_async(room.save)
        # await save_room_async()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "username": user.nickname,
                "message": chat_message,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        nickname = event["username"]

        await self.send(
            text_data=json.dumps({"username": nickname, "message": message})
        )

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from rest_framework.response import Response
from channels.db import database_sync_to_async

from .models import Rooms, Room_members, Messages
from .cache import get_user_by_id_from_cache

from datetime import datetime
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()
env = os.environ.get

# 전역 변수로 MongoDB 연결 객체 설정
MONGODB_CLIENT = AsyncIOMotorClient(
    host=env("MONGO_DB_HOST"),
    port=int(env("MONGO_DB_PORT")),
)
db = MONGODB_CLIENT[env("MONGO_DB_NAME")]

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    return get_user_by_id_from_cache(user_id)


async def save_message(room, user, message):
    try:
        messages_collection = db["chat_messages"]
        inserted_message = await messages_collection.insert_one(
            {
                "user": user.pk,
                "room_id": room["id"],
                "message": message,
                "created_at": datetime.now(),
            }
        )

        rooms_collection = db["chat_rooms"]
        rooms_collection.update_one(
            {"_id": room["_id"]},
            {"$set": {"updated_at": datetime.now(), "lastest_text": message}},
        )

        return {
            "action": "message",
            "user": user.id,
            "roomname": room["room_name"],
            "message": message,
            "userprofile": user.image_url.url if user.image_url else None,
            "username": user.nickname,
            "created_at": str(inserted_message.inserted_id.generation_time),
        }
    except Exception as e:
        print("생성실패", e)
        return None


async def get_user_from_cookie(self):
    try:
        token = self.scope["cookies"]["access_token"]
        user_id = AccessToken(token)["user_id"]
        user = await get_user(user_id)
        return user

    except TokenError:
        await self.close()
        return Response({"error": "토큰만료"}, status=401)


async def get_room(room_name):
    rooms_collection = db["chat_rooms"]

    room = await rooms_collection.find_one({"room_name": room_name})
    if room:
        # Room_members 컬렉션 업데이트
        room_members_collection = db["chat_room_members"]
        await room_members_collection.update_many(
            {"room_id": room["id"]}, {"$set": {"is_visibled": True}}
        )

        return room
    return None

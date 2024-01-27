from .models import Rooms, Messages, Room_members
from .cache import get_user_by_id_from_cache

from rest_framework import serializers
from core.permissions import get_user_id
from django.contrib.auth import get_user_model

import random
import string


User = get_user_model()


class RoomSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()

    class Meta:
        model = Rooms
        fields = ["other_user", "room_name", "lastest_text", "updated_at"]

    def get_other_user(self, room):
        request = self.context.get("request")
        user_id = get_user_id(request)
        member_ids = room.visibility.exclude(user=user_id).values_list(
            "user", flat=True
        )
        other_members = [
            get_user_by_id_from_cache(member_id) for member_id in member_ids
        ]

        return [
            {
                "nickname": member.nickname,
                "profile_img": request.build_absolute_uri(member.image_url.url)
                if member.image_url
                else None,
            }
            for member in other_members
        ]


class RoomCreateSerializer(serializers.ModelSerializer):
    room = serializers.SerializerMethodField()

    class Meta:
        model = Rooms
        fields = ["room"]

    def get_room(self, obj):
        request = self.context.get("request")
        user_id = get_user_id(request)
        other_user_id = request.data.get("user", "")

        try:
            User.objects.get(pk=other_user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("해당하는 유저를 찾을 수 없습니다.")

        # 이미 같은 채팅방이 존재하는지 확인
        existing_rooms = Room_members.objects.filter(
            user=user_id, room__visibility__user=other_user_id
        )
        if existing_rooms:
            # Room_members > Rooms > room_name
            room_names = [room.room.room_name for room in existing_rooms]
            existing_rooms.update(is_visibled=True)
            raise serializers.ValidationError(
                {
                    "room_name": room_names,
                    "message": "이미 해당 사용자와 채팅방이 있습니다. 메세지를 보내 채팅을 시작하세요.",
                }
            )

        user = User.objects.get(pk=user_id)
        other_user = User.objects.get(pk=other_user_id)

        room_name = self.generate_random_room_name()
        room = Rooms.objects.create(room_name=room_name)

        Room_members.objects.create(user=user.pk, room=room)
        Room_members.objects.create(user=other_user.pk, room=room)

        return {
            "room_name": room_name,
            "room": f"{user.nickname}, {other_user.nickname}",
        }

    def generate_random_room_name(self):
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=20))


class MessageSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="user.nickname", read_only=True)
    image_url = serializers.ImageField(source="user.image_url", read_only=True)
    is_sender = serializers.SerializerMethodField()

    class Meta:
        model = Messages
        fields = ["is_sender", "nickname", "image_url", "message", "created_at"]

    def get_is_sender(self, obj):
        request = self.context.get("request")
        user_id = get_user_id(request)

        return obj.user == user_id

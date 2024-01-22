from djongo import models
from core.models import TimestampedModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Rooms(models.Model):
    room_name = models.CharField(max_length=50)
    lastest_text = models.TextField("마지막 대화")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Room_members(models.Model):
    user = models.IntegerField(unique=True)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name="visibility")
    is_visibled = models.BooleanField(default=True)


class Messages(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name="rooms")
    user = models.IntegerField(unique=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.nickname}: {self.message}"

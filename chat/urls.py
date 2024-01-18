from django.urls import path
from .views import (
    RoomListAPIView,
    MessageListAPIView,
    RoominvisibleAPIView,
    RoomCreateAPIView,
    mongoview,
)


urlpatterns = [
    path("mongo/", mongoview.as_view()),
    path("roomlist/", RoomListAPIView.as_view(), name="roomlist"),
    path("roomcreate/", RoomCreateAPIView.as_view(), name="room_create"),
    path(
        "roominvisible/<str:room_name>/",
        RoominvisibleAPIView.as_view(),
        name="room_invisible",
    ),
    path("<str:room_name>/", MessageListAPIView.as_view(), name="room_message"),
]

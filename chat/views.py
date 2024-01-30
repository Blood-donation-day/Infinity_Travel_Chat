from .models import Rooms, Messages, Room_members
from .serializers import *
from .mongo import test

from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from core.permissions import get_user_id


class mongoview(APIView):
    def get(self, request):
        test()
        user_id = get_user_id(self.request)
        print(user_id, "테스트뷰")
        return Response("ㅎㅇ")


class RoomListAPIView(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        user_id = get_user_id(self.request)
        try:
            room_members = Room_members.objects.filter(user=user_id)
            rooms = room_members.values_list("room", flat=True)
            queryset = Rooms.objects.filter(id__in=rooms)

        except Exception as e:
            print(f"Error: {e}")
            queryset = Rooms.objects.none()

        return queryset


class RoomCreateAPIView(generics.CreateAPIView):
    serializer_class = RoomCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoominvisibleAPIView(APIView):
    def get(self, request, room_name):
        user_id = get_user_id(request)
        try:
            room = Rooms.objects.get(room_name=room_name)
            member = Room_members.objects.get(room=room.pk, user=user_id)
            member.is_visibled = False
            member.save()
            return Response(
                {"message": "채팅방을 삭제했습니다."},
                status=status.HTTP_200_OK,
            )
        except Rooms.DoesNotExist:
            return Response(
                {"error": "해당하는 채팅방을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )


class MessageListPagination(PageNumberPagination):
    page_size = 30
    # 개수를 지정하여 불러올 때
    page_size_query_param = "page_size"
    max_page_size = 200


class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    pagination_class = MessageListPagination

    def get_queryset(self):
        user_id = get_user_id(self.request)
        room_name = self.kwargs.get("room_name", "")
        room = get_object_or_404(Rooms, room_name=room_name)
        queryset = Messages.objects.filter(room=room).order_by("-created_at")
        return queryset

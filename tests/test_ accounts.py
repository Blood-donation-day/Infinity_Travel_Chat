from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()
room_name = "1_2"
email = "test12@test12.com"
password = "testpw123"
loginurl = "/accounts/login/"
token_refresh_url = "/accounts/refresh/"
profileurl = "/accounts/"
testmessage = "hello world"


class MyTests(TestCase):
    def setUp(self):
        print("----------유저 생성-----------")
        self.user = User.objects.create_user(
            email=email,
            password=password,
            gender="Male",
            nickname="test",
            birth="2023-11-11",
        )
        self.user2 = User.objects.create_user(
            email="test222@test22.com",
            password="testpassword2222",
            gender="Male",
            nickname="test",
            birth="2023-11-11",
        )

        client = Client()
        response = self.client.post(loginurl, {"email": email, "password": password})

    def test_login_user(self):
        print("----------로그인 테스트-----------")

        response = self.client.post(loginurl, {"email": email, "password": password})
        print(response.data.get("message"))
        self.assertEqual(response.status_code, 200)

    def test_refresh_token(self):
        print("----------토큰 갱신 테스트-----------")

        response = self.client.post(token_refresh_url)
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        print("----------내 프로필 테스트-----------")

        response = self.client.get(profileurl)
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_profile_change(self):
        print("----------프로필 수정 테스트-----------")

        response = self.client.patch(
            profileurl,
            {"nickname": "닉네임변경", "birth": "2020-11-11", "introduction": "자기소개"},
            content_type="application/json",
        )
        print(response.data)
        nickname = response.data.get("nickname")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(nickname, "닉네임변경")

    def test_zdelete_user(self):
        print("----------회원탈퇴 테스트-----------")

        response = self.client.delete(profileurl)
        print(response.data)
        self.assertEqual(response.status_code, 204)

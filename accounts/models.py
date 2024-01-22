from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from core.models import TimestampedModel


class UserManager(BaseUserManager):
    def create_user(
        self, email, gender, nickname, birth, password=None, **extra_fields
    ):
        if email == None:
            raise TypeError("이메일은 필수값입니다.")
        if password is None:
            raise TypeError("비밀번호는 필수값입니다.")

        user = self.model(
            email=self.normalize_email(email),
            gender=gender,
            nickname=nickname,
            birth=birth,
            **extra_fields,
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, gender, nickname, birth, password):
        user = self.create_user(email, gender, nickname, birth, password)

        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    email = models.EmailField(max_length=100, db_index=True, unique=True)
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    GENDER = [("Male", "남자"), ("Female", "여자"), ("None", "선택없음")]
    gender = models.CharField(max_length=6, choices=GENDER)
    nickname = models.CharField(max_length=20)
    birth = models.DateField()
    introduction = models.TextField(blank=True)
    image_url = models.ImageField(upload_to="accounts/image_url/%y/%m%d", blank=True)
    REQUIRED_FIELDS = ["password", "gender", "nickname", "birth"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.nickname:
            return self.nickname
        return None

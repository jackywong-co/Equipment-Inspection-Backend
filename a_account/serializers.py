from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from a_account.models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])

        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.UUIDField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'token')

        read_only_fields = ['token']
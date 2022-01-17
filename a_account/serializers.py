from rest_framework import serializers
from a_account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.UUIDField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'token')

        read_only_fields = ['token']

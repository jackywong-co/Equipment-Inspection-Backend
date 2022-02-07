from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from a_account.models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            is_staff=validated_data['is_staff']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'is_staff', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        return token

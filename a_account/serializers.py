from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from a_account.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    username = serializers.CharField(max_length=150, required=False)
    password = serializers.CharField(max_length=128, required=False)
    is_staff = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(default=True)

    def create(self, validated_data):

        user = User(
            username=validated_data['username'],
            is_staff=validated_data['is_staff']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    # class Meta:
    #     model = User
    #     # fields = ('id', 'username', 'password', 'is_staff', 'is_active')
    #     fields = '__all__'
    #     extra_kwargs = {
    #         'password': {'write_only': True}
    #     }


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        return token

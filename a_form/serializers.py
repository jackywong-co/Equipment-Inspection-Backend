from rest_framework import serializers
from a_form.models import Room


class RoomSerializer(serializers.Serializer):
    roomId = serializers.UUIDField(required=False)
    roomName = serializers.CharField()
    location = serializers.CharField()
    status = serializers.CharField(required=False)
    createdAt = serializers.DateTimeField(required=False)
    modifiedAt = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return Room.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.roomName = validated_data.get('roomName', instance.roomName)
        instance.location = validated_data.get('location', instance.location)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

# class FormSerializer(serializers.Serializer):
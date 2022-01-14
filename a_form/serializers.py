from rest_framework import serializers
from .models import *


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username']
#
#
# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ['questionText', 'status', 'createdAt', 'modifiedAt']
#
#
# class FormForEquipmentSerializer(serializers.ModelSerializer):
#     questions = QuestionSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Form
#         fields = ['formName', 'createdBy', 'questions', 'status', 'createdAt', 'modifiedAt']
#
#     def create(self, validated_data):
#         return Form.objects.create(**validated_data)
#
#
# class EquipmentFormSerializer(serializers.ModelSerializer):
#     forms = FormForEquipmentSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Equipment
#         fields = ['forms']
#
#
# class EquipmentSerializer(serializers.ModelSerializer):
#     roomName = serializers.CharField(read_only=True, source="room.roomName")
#     forms = EquipmentFormSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Equipment
#         fields = ['equipmentId', 'equipmentName', 'room', 'roomName', 'ThisInspectionOn', 'NextInspectionOn', 'status',
#                   'createdAt',
#                   'modifiedAt',
#                   'forms']
#
#
# class FormSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Form
#         fields = ['formName', 'createdBy', 'status', 'createdAt', 'modifiedAt']
#
#     def create(self, validated_data):
#         return Form.objects.create(**validated_data)


# class RoomSerializer(serializers.ModelSerializer):
#     equipments = EquipmentSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Room
#         fields = ['roomId', 'roomName', 'location', 'equipments', 'status', 'createdAt', 'modifiedAt']

class RoomSerializer(serializers.Serializer):
    roomId = serializers.UUIDField(read_only=True)
    roomName = serializers.CharField(required=True, allow_blank=True)
    location = serializers.CharField(max_length=30)
    createdAt = serializers.DateTimeField(auto_now_add=True)
    modifiedAt = serializers.DateTimeField(auto_now=True)


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=True, max_length=90)
    body = serializers.CharField(required=False, allow_blank=True)
    author = serializers.ReadOnlyField(source="author.id")
    status = serializers.ChoiceField(choices=Article.STATUS_CHOICES, default='p')
    create_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        Create a new "article" instance
        """
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Use validated data to return an existing `Article`instance。"""
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
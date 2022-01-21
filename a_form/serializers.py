from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from a_account.models import User
from a_account.serializers import UserSerializer
from a_form.models import Room, Equipment, Form, Question


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'


class EquipmentSerializer(serializers.Serializer):
    equipmentId = serializers.UUIDField(required=False)
    equipmentName = serializers.CharField()
    equipmentCode = serializers.CharField(required=False)
    # roomId = serializers.SlugRelatedField(many=True,   read_only=True, slug_field='room')

    ThisInspectionOn = serializers.DateTimeField(required=False)
    NextInspectionOn = serializers.DateTimeField(required=False)
    status = serializers.CharField(required=False)
    createdAt = serializers.DateTimeField(required=False)
    modifiedAt = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return Equipment.objects.create(**validated_data)


class RoomSerializer(serializers.Serializer):
    roomId = serializers.UUIDField(required=False)
    roomName = serializers.CharField()
    location = serializers.CharField()
    equipments = EquipmentSerializer(many=True, required=False)

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


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class FormSerializer(serializers.ModelSerializer):
    equipments = EquipmentSerializer(many=True)
    questions = QuestionSerializer(many=True)

    def create(self, validated_data):
        equipment_data = validated_data.pop('equipment')
        form = Form.objects.create(**validated_data)
        Equipment.objects.create(form=form, **equipment_data)
        return form

    class Meta:
        model = Form
        fields = ['formName', 'createdBy', 'equipments', 'questions']

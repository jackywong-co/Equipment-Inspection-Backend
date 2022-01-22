from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from a_account.models import User
from a_account.serializers import UserSerializer
from a_form.models import Room, Equipment, Form, Question, FormEquipment, FormQuestion


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    # id = serializers.UUIDField(required=False)
    # room_name = serializers.CharField()
    #
    # location = serializers.CharField()
    # equipments = EquipmentSerializer(many=True, required=False)
    #
    # status = serializers.CharField(required=False)
    # created_at = serializers.DateTimeField(required=False)
    # modified_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return Room.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.room_name = validated_data.get('room_name', instance.room_name)
        instance.location = validated_data.get('location', instance.location)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    class Meta:
        model = Room
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class FormQuestionSerializer(serializers.Serializer):
    questionId = serializers.UUIDField()
    formId = serializers.UUIDField()

    def create(self, validated_data):
        return FormQuestion.objects.create(**validated_data)


class FormSerializer(serializers.ModelSerializer):
    # equipments = FormEquipmentSerializer(many=True, required=False)
    # questions = FormQuestionSerializer(many=True, required=False)

    def create(self, validated_data):
        return Form.objects.create(**validated_data)

    class Meta:
        model = Form
        fields = ['formId', 'formName', 'createdBy', 'equipments', 'questions']


class FormEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormEquipment
        fields = '__all__'

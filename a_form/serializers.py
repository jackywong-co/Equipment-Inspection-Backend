from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from a_account.models import User
from a_account.serializers import UserSerializer
from a_form.models import Room, Equipment, Form, Question, FormEquipment, FormQuestion, Answer, AnswerQuestion


class RoomSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    room_name = serializers.CharField(max_length=30, required=False)
    location = serializers.CharField(max_length=30, required=False)
    is_active = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return Room.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.room_name = validated_data.get('room_name', instance.room_name)
        instance.location = validated_data.get('location', instance.location)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    # class Meta:
    #     model = Room
    #     fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    equipment_name = serializers.CharField(max_length=30, required=False)
    equipment_code = serializers.CharField(max_length=30, required=False)
    room = RoomSerializer(required=False)
    is_active = serializers.BooleanField(default=True)

    def create(self, validated_data):
        print(validated_data)
        return Equipment.objects.create(**validated_data)

    class Meta:
        model = Equipment
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class FormQuestionObjectSerializer(serializers.Serializer):
    questionId = serializers.UUIDField()
    formId = serializers.UUIDField()

    def create(self, validated_data):
        return FormQuestion.objects.create(**validated_data)


class FormQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text']


class FormEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_code']


class FormUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class FormSerializer(serializers.ModelSerializer):
    created_by = FormUserSerializer()
    equipments = FormEquipmentSerializer(many=True)
    questions = FormQuestionSerializer(many=True)

    def create(self, validated_data):
        return Form.objects.create(**validated_data)

    class Meta:
        model = Form
        fields = '__all__'


class FormEquipmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormEquipment
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    created_by = UserSerializer(required=False)
    form = FormSerializer(required=False)
    class Meta:
        model = Answer
        fields = '__all__'

class AnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerQuestion
        fields = '__all__'

from django.http import Http404
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from a_form.serializers import RoomSerializer, EquipmentSerializer, FormSerializer, QuestionSerializer, \
    FormEquipmentSerializer, FormQuestionSerializer
from a_form.models import Room, Equipment, Form, FormEquipment, Question, FormQuestion
from a_account.serializers import UserSerializer
from a_account.models import User
from rest_framework import status


# Create your views here.
class UserView(APIView):

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class RoomView(APIView):

    def get(self, request):
        room = Room.objects.all()
        serializer = RoomSerializer(room, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetailView(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        room = self.get_object(pk)
        room.delete()
        return Response({"message": "deleted"}, status=status.HTTP_204_NO_CONTENT)


class EquipmentView(APIView):

    def get(self, request):
        equipment = Equipment.objects.all()
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EquipmentDetailView(APIView):

    def get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        equipment = self.get_object(pk)
        serializer = EquipmentSerializer(equipment)
        equipment_obj = serializer.data

        forms_arr = []
        form_equipments = FormEquipment.objects.filter(equipment=equipment)

        for form_equipment in form_equipments:
            serializer = FormSerializer(form_equipment.form)
            forms_arr.append(serializer.data)

        equipment_obj['forms'] = forms_arr

        return Response(equipment_obj)

    def put(self, request, pk):
        equipment = self.get_object(pk)
        serializer = EquipmentSerializer(equipment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        equipment = self.get_object(pk)
        equipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FormView(APIView):

    def get(self, request):
        form = Form.objects.all()
        serializer = FormSerializer(form, many=True)
        return Response(serializer.data)

    def post(self, request):
        form_name = request.data['form_name']
        user = User.objects.get(id=request.data['created_by'])
        created_by = user
        form = Form.objects.create(form_name=form_name, created_by=created_by)

        form.save()

        equipments = request.data['equipments']
        questions = request.data['questions']

        # print(formName)
        form_id = Form.objects.get(id=form.id)
        for equipment in equipments:
            equipment_id = Equipment.objects.get(id=equipment)
            form_equipment = FormEquipment.objects.create(form=form_id, equipment=equipment_id)
            form_equipment.save()
        for questions in questions:
            question_id = Question.objects.get(id=questions)
            form_question = FormQuestion.objects.create(form=form_id, question=question_id)
            form_question.save()

        return Response({"message": "form created"})


class FormDetailView(APIView):

    def get_object(self, pk):
        try:
            return Form.objects.get(pk=pk)
        except Form.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        form = self.get_object(pk)
        serializer = FormSerializer(form)
        return Response(serializer.data)

    def put(self, request, pk):
        form = self.get_object(pk)
        serializer = FormSerializer(form, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        form = self.get_object(pk)
        form.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FormEquipmentView(APIView):

    def get(self, request):
        form_equipment = FormEquipment.objects.all()
        serializer = FormEquipmentSerializer(form_equipment, many=True)
        return Response(serializer.data)


class FormEquipmentDetailView(APIView):

    def get_object(self, pk):
        try:
            return FormEquipment.objects.get(pk=pk)
        except FormEquipment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        form_equipment = self.get_object(pk)
        serializer = FormSerializer(form_equipment)
        return Response(serializer.data)


class FormQuestionView(APIView):

    def get(self, request):
        form_question = FormQuestion.objects.all()
        serializer = FormEquipmentSerializer(form_question, many=True)
        return Response(serializer.data)


class FormQuestionDetailView(APIView):

    def get_object(self, pk):
        try:
            return FormQuestion.objects.get(pk=pk)
        except FormQuestion.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        form_question = self.get_object(pk)
        serializer = FormQuestionSerializer(form_question)
        return Response(serializer.data)


class QuestionView(APIView):

    def get(self, request):
        question = Question.objects.all()
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(TemplateView):
    template_name = "login.html"


class DashboardView(TemplateView):
    template_name = "dashboard.html"

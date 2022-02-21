from django.http import Http404
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from a_api.permissions import ManagerPermission
from a_form.serializers import (RoomSerializer, EquipmentSerializer, FormSerializer, QuestionSerializer,
                                AnswerSerializer, FormEquipmentSerializer, FormQuestionSerializer)
from a_form.models import (Room, Equipment, Form, Question, Answer, FormEquipment, FormQuestion)
from a_account.serializers import UserSerializer
from a_account.models import User
from rest_framework import status


# Create your views here.
class UserView(APIView):
    permission_classes = [ManagerPermission]

    def get(self, request):
        print(UserSerializer(request.user).data["id"])
        user = User.objects.filter(is_superuser=False).filter(~Q(id=UserSerializer(request.user).data["id"]))
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    permission_classes = [ManagerPermission]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response({"message": "deleted"}, status=status.HTTP_204_NO_CONTENT)


class RoomView(APIView):
    permission_classes = [ManagerPermission]

    def get(self, request):
        room_all = Room.objects.all()
        room_arr = []
        for room in room_all:
            room_arr.append(
                {"id": room.id, "room_name": room.room_name,
                 "location": room.location, "is_active": room.is_active})
        return Response(room_arr)

    def post(self, request):
        room_data = request.data
        room_name = room_data["room_name"]
        location = room_data["location"]
        Room.objects.create(room_name=room_name, location=location)
        return Response({"message": "room created"}, status=status.HTTP_204_NO_CONTENT)


class RoomDetailView(APIView):
    permission_classes = [ManagerPermission]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        room = self.get_object(pk)
        return Response({"id": room.id, "room_name": room.room_name,
                         "location": room.location, "is_active": room.is_active})

    def put(self, request, pk):
        room = Room.objects.get(id=pk)
        room_data = request.data
        if "room_name" in room_data:
            room.room_name = room_data["room_name"]
        else:
            room.room_name = room.room_name
        if "location" in room_data:
            room.location = room_data["location"]
        else:
            room.location = room.location
        if "is_active" in room_data:
            room.is_active = room_data["is_active"]
        else:
            room.is_active = room.is_active
        if "room_id" in room_data:
            room.id = room_data["room_id"]
        else:
            room.id = room.id
        room.save()
        return Response({"message": "room updated"}, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        room = self.get_object(pk)
        room.delete()
        return Response({"message": "deleted"}, status=status.HTTP_204_NO_CONTENT)


class EquipmentView(APIView):
    permission_classes = [ManagerPermission]

    def get(self, request):
        equipment_all = Equipment.objects.all()
        equipment_arr = []
        for equipment in equipment_all:
            equipment_arr.append(
                {"equipment_id": equipment.id, "equipment_name": equipment.equipment_name,
                 "equipment_code": equipment.equipment_code, "is_active": equipment.is_active,
                 "room_id": equipment.room.id,
                 "room_name": equipment.room.room_name})
        return Response(equipment_arr)

    def post(self, request):
        equipment_data = request.data
        equipment_name = equipment_data["equipment_name"]
        equipment_code = equipment_data["equipment_code"]
        room = Room.objects.get(id=equipment_data["room"])
        Equipment.objects.create(equipment_name=equipment_name, equipment_code=equipment_code, room=room)
        return Response({"message": "equipment created"}, status=status.HTTP_204_NO_CONTENT)


class EquipmentDetailView(APIView):
    permission_classes = [ManagerPermission]

    def get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        equipment = self.get_object(pk)
        if equipment in FormEquipment.objects.all():
            form_equipment = FormEquipment.objects.get(equipments=equipment)
            form_id = form_equipment.forms.id
            form_name = form_equipment.forms.form_name
        else:
            form_id = ""
            form_name = ""
        return Response({"equipment_id": equipment.id, "equipment_name": equipment.equipment_name,
                         "equipment_code": equipment.equipment_code, "is_active": equipment.is_active,
                         "room_id": equipment.room.id, "room_name": equipment.room.room_name,
                         "form_id": form_id, "form_name": form_name
                         })

    def put(self, request, pk):
        equipment = self.get_object(pk)
        equipment_data = request.data
        if "equipment_name" in equipment_data:
            equipment.equipment_name = equipment_data["equipment_name"]
        else:
            equipment.equipment_name = equipment.equipment_name
        if "equipment_code" in equipment_data:
            equipment.equipment_code = equipment_data["equipment_code"]
        else:
            equipment.equipment_code = equipment.equipment_code
        if "is_active" in equipment_data:
            equipment.is_active = equipment_data["is_active"]
        else:
            equipment.is_active = equipment.is_active
        if "room_id" in equipment_data:
            equipment.room_id = equipment_data["room_id"]
        else:
            equipment.room_id = equipment.room_id
        equipment.save()
        return Response({"message": "equipment updated"}, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        equipment = self.get_object(pk)
        equipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FormView(APIView):
    permission_classes = [ManagerPermission]

    def get(self, request):
        form_all = Form.objects.all()
        form_arr = []
        for form in form_all:
            form_equipment = FormEquipment.objects.filter(forms=form.id)
            equipment_arr = []
            for form_equipment in form_equipment:
                equipment_arr.append(
                    {"equipment_id": form_equipment.equipments.id,
                     "equipment_name": form_equipment.equipments.equipment_name,
                     "equipment_code": form_equipment.equipments.equipment_code,
                     "room_id": form_equipment.equipments.room.id,
                     "room_name": form_equipment.equipments.room.room_name,
                     }
                )
            form_question = FormQuestion.objects.filter(forms=form.id)
            question_arr = []
            for form_questions in form_question:
                question_arr.append(
                    {"question_id": form_questions.questions.id,
                     "question_text": form_questions.questions.question_text}
                )
            form_arr.append(
                {"form_id": form.id,
                 "form_name": form.form_name,
                 "created_by": form.created_by.id,
                 "equipments": equipment_arr,
                 "questions": question_arr,
                 "is_active": form.is_active})
        return Response(form_arr)

    def post(self, request):
        form_name = request.data['form_name']
        user = User.objects.get(id=request.data['created_by'])
        created_by = user
        form = Form.objects.create(form_name=form_name, created_by=created_by)
        form.save()
        equipments = request.data['equipments']
        questions = request.data['questions']

        form_id = Form.objects.get(id=form.id)
        for equipment in equipments:
            equipment_id = Equipment.objects.get(id=equipment)
            form_equipment = FormEquipment.objects.create(forms=form_id, equipments=equipment_id)
            form_equipment.save()
        for questions in questions:
            question_id = Question.objects.get(id=questions)
            form_question = FormQuestion.objects.create(forms=form_id, questions=question_id)
            form_question.save()

        return Response({"message": "form created"})


class FormDetailView(APIView):
    permission_classes = [ManagerPermission]

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
    permission_classes = [ManagerPermission]

    def get(self, request):
        form_equipment = FormEquipment.objects.all()
        serializer = FormEquipmentSerializer(form_equipment, many=True)
        return Response(serializer.data)


class FormEquipmentDetailView(APIView):
    permission_classes = [ManagerPermission]

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
    permission_classes = [ManagerPermission]

    def get(self, request):
        form_question = FormQuestion.objects.all()
        serializer = FormEquipmentSerializer(form_question, many=True)
        return Response(serializer.data)


class FormQuestionDetailView(APIView):
    permission_classes = [ManagerPermission]

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
    permission_classes = [ManagerPermission]

    def get(self, request):
        question_all = Question.objects.all()
        question_arr = []
        for question in question_all:
            question_arr.append(
                {"id": question.id, "question_text": question.question_text, "is_active": question.is_active})
        return Response(question_arr)

    def post(self, request):
        question_data = request.data
        question_text = question_data["question_text"]
        Question.objects.create(question_text=question_text)
        return Response({"message": "question created"}, status=status.HTTP_204_NO_CONTENT)


class QuestionDetailView(APIView):
    permission_classes = [ManagerPermission]

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        question = self.get_object(pk)
        return Response({"id": question.id, "question_text": question.question_text,
                         "is_active": question.is_active})

    def put(self, request, pk):

        question = self.get_object(pk)
        question_data = request.data
        if "question_text" in question_data:
            question.question_text = question_data["question_text"]
        else:
            question.question_text = question.question_text
        if "is_active" in question_data:
            question.is_active = question_data["is_active"]
        else:
            question.is_active = question.is_active
        if "id" in question_data:
            question.id = question_data["id"]
        else:
            question.id = question.id
        question.save()
        return Response({"message": "question updated"}, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        question = self.get_object(pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerView(APIView):
    permission_classes = [ManagerPermission]

    def get(self, request):
        answer = Answer.objects.all()
        serializer = AnswerSerializer(answer, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerDetailView(APIView):
    permission_classes = [ManagerPermission]

    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        answer = self.get_object(pk)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)

    def put(self, request, pk):
        answer = self.get_object(pk)
        serializer = AnswerSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        answer = self.get_object(pk)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

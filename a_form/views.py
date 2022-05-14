import io
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from django.db.models import Count
from django.http import Http404, FileResponse
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from a_api.permissions import ManagerPermission
from a_form.serializers import (RoomSerializer, EquipmentSerializer, FormSerializer, QuestionSerializer,
                                AnswerSerializer, FormEquipmentSerializer, FormQuestionSerializer,
                                EquipmentImageSerializer)
from a_form.models import (Room, Equipment, Form, Question, Answer, FormEquipment, FormQuestion, AnswerQuestion,
                           EquipmentImage, UniqueId)
from a_account.serializers import UserSerializer
from a_account.models import User
from rest_framework import status
from sys import getsizeof
# create pdf
from reportlab import platypus


def remove_first_end_spaces(string):
    return "".join(string.rstrip().lstrip())


# Create your views here.
class UserView(APIView):
    permission_classes = [ManagerPermission]

    def get(self, request):
        user = User.objects.filter(is_superuser=False)
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
            equipment_arr = []
            for equipment in Equipment.objects.filter(room=room):
                equipment_arr.append(
                    {
                        "equipment_id": equipment.id,
                        "equipment_name": equipment.equipment_name.replace("_", " "),
                        "equipment_code": equipment.equipment_code
                    }
                )
            room_arr.append(
                {
                    "id": room.id,
                    "room_name": room.room_name.replace("_", " "),
                    "location": room.location,
                    "equipments": equipment_arr,
                    "is_active": room.is_active
                }
            )
        return Response(room_arr)

    def post(self, request):
        room_data = request.data
        room_name = room_data["room_name"]
        room_name = remove_first_end_spaces(room_name).replace(" ", "_")
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
        equipment_arr = []
        for equipment in Equipment.objects.filter(room=room):
            equipment_arr.append(
                {
                    "equipment_id": equipment.id,
                    "equipment_name": equipment.equipment_name.replace("_", " "),
                    "equipment_code": equipment.equipment_code,
                    "is_active": equipment.is_active,
                    "room_id": equipment.room.id,
                    "room_name": equipment.room.room_name.replace("_", " ")
                }
            )
        return Response(
            {
                "id": room.id,
                "room_name": room.room_name.replace("_", " "),
                "location": room.location,
                "equipments": equipment_arr,
                "is_active": room.is_active
            }
        )

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
                {
                    "equipment_id": equipment.id,
                    "equipment_name": equipment.equipment_name.replace("_", " "),
                    "equipment_code": equipment.equipment_code,
                    "is_active": equipment.is_active,
                    "room_id": equipment.room.id,
                    "room_name": equipment.room.room_name.replace("_", " ")
                }
            )
        return Response(equipment_arr)

    def post(self, request):
        equipment_data = request.data
        equipment_name = equipment_data["equipment_name"]
        equipment_name = remove_first_end_spaces(equipment_name).replace(" ", "_")
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
        if FormEquipment.objects.filter(equipments=equipment):
            form_equipment = FormEquipment.objects.get(equipments=equipment)
            form_id = form_equipment.forms.id
            form_name = form_equipment.forms.form_name
        else:
            form_id = ""
            form_name = ""
        return Response(
            {
                "equipment_id": equipment.id,
                "equipment_name": equipment.equipment_name,
                "equipment_code": equipment.equipment_code,
                "is_active": equipment.is_active,
                "room_id": equipment.room.id,
                "room_name": equipment.room.room_name,
                "form_id": form_id,
                "form_name": form_name
            }
        )

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


class EquipmentImageView(APIView):
    permission_classes = [ManagerPermission]

    def post(self, request):
        print(request.data)
        pic = request.data["image"]
        img = Image.open(pic)
        pic_io = BytesIO()
        img.save(pic_io, format='PNG')
        pic_io.seek(0)
        pic_file = InMemoryUploadedFile(
            file=pic_io,
            field_name=None,
            name="%s.png" % pic.name.split('.')[0],
            content_type='image/png',
            size=getsizeof(pic_io),
            charset=None,
        )
        equipment = Equipment.objects.get(id=request.data['equipment'])
        equipmentImage = EquipmentImage.objects.create(equipment=equipment, image=pic_file)
        equipmentImage.save()

        return Response({"message": "Equipment Image Upload Success"})


class FormView(APIView):
    permission_classes = [ManagerPermission]

    def get(self, request):
        form_all = Form.objects.all()
        form_arr = []
        for form in form_all:
            user = {
                "id": form.created_by.id,
                "username": form.created_by.username
            }
            form_equipment = FormEquipment.objects.filter(forms=form.id)
            equipment_arr = []
            for form_equipment in form_equipment:
                equipment_arr.append(
                    {
                        "equipment_id": form_equipment.equipments.id,
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
                    {
                        "question_id": form_questions.questions.id,
                        "question_text": form_questions.questions.question_text
                    }
                )
            unique_id = UniqueId.objects.create();
            form_arr.append(
                {
                    "form_id": form.id,
                    "form_name": form.form_name,
                    "unique_id": unique_id.id,
                    "created_by": user,
                    "equipments": equipment_arr,
                    "questions": question_arr,
                    "is_active": form.is_active
                }
            )
        return Response(form_arr)

    def post(self, request):
        form_name = request.data['form_name']
        user = User.objects.get(id=request.data['created_by'])
        created_by = user
        form = Form.objects.create(form_name=form_name, created_by=created_by)
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
        form_equipment = FormEquipment.objects.filter(forms=form.id)
        equipment_arr = []
        for form_equipment in form_equipment:
            equipment_arr.append(
                {
                    "equipment_id": form_equipment.equipments.id,
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
                {
                    "question_id": form_questions.questions.id,
                    "question_text": form_questions.questions.question_text
                }
            )
        return Response(
            {"form_id": form.id,
             "form_name": form.form_name,
             "created_by_id": form.created_by.id,
             "created_by_name": form.created_by.username,
             "equipments": equipment_arr,
             "questions": question_arr,
             "is_active": form.is_active
             }
        )

    def put(self, request, pk):
        form = self.get_object(pk)
        form_data = request.data
        if "form_name" in form_data:
            form.form_name = form_data["form_name"]
        else:
            form.form_name = form.form_name

        if "created_by_id" in form_data:
            form.created_by = form_data["created_by_id"]
        else:
            form.created_by = form.created_by

        if "equipments" in form_data:
            for equipment in form_data["equipments"]:
                equipment_obj = Equipment.objects.get(id=equipment)
                form_equipment = FormEquipment.objects.get(forms_id=pk)
                form_equipment.equipments = equipment_obj
                form_equipment.save()
        # else:
        #     form.equipments = form.equipments

        if "is_active" in form_data:
            form.is_active = form_data["is_active"]
        else:
            form.is_active = form.is_active

        form.save()
        return Response({"message": "form updated"}, status=status.HTTP_204_NO_CONTENT)

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
                {
                    "id": question.id,
                    "question_text": question.question_text,
                    "is_active": question.is_active
                }
            )
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
        response = {
            "id": question.id,
            "question_text": question.question_text,
            "is_active": question.is_active
        }
        return Response(response)

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
        return Response({"message": "question updated"})

    def delete(self, request, pk):
        question = self.get_object(pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerView(APIView):
    permission_classes = [ManagerPermission]

    def get(self, request):
        answer_all = Answer.objects.all()
        answer_arr = []
        for answer in answer_all:
            answer_question = AnswerQuestion.objects.get(answers=answer)
            question = Question.objects.get(id=answer_question.questions.id)
            if answer.image:
                image = answer.image.url
            else:
                image = ""
            if answer.signature:
                signature = answer.signature.url
            else:
                signature = ""
            form_equipment = FormEquipment.objects.get(forms=answer.form)
            equipment = Equipment.objects.get(id=form_equipment.equipments.id)
            answer_arr.append(
                {
                    "id": answer.id,
                    "answer_text": answer.answer_text,
                    "image": image,
                    "signature": signature,
                    "unique_id": answer.unique_id.id,
                    "created_by": {
                        "id": answer.created_by_id,
                        "username": answer.created_by.username
                    },
                    "form_id": answer.form.id,
                    "form_name": answer.form.form_name,
                    "equipment_id": equipment.id,
                    "equipment_code": equipment.equipment_code,
                    "equipment_name": equipment.equipment_name.replace("_", " "),
                    "room_id": equipment.room.id,
                    "room_name": equipment.room.room_name.replace("_", " "),
                    "room_location": equipment.room.location,
                    "question_id": question.id,
                    "question_text": question.question_text,
                    "is_active": answer.is_active,
                    "created_at": answer.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            )
        return Response(answer_arr)

    def post(self, request):
        answer_text = request.data['answer_text']
        unique_id = request.data['unique_id']
        unique_id = UniqueId.objects.get(id=unique_id)
        if 'image' in request.data:
            pic = request.data['image']
            img = Image.open(pic)
            pic_io = BytesIO()
            img.save(pic_io, format='PNG')
            pic_io.seek(0)
            pic_file = InMemoryUploadedFile(
                file=pic_io,
                field_name=None,
                name="%s.png" % pic.name.split('.')[0],
                content_type='image/png',
                size=getsizeof(pic_io),
                charset=None,
            )
        else:
            pic_file = ""
        if "signature" in request.data:
            pic = request.data['signature']
            img = Image.open(pic)
            pic_io = BytesIO()
            img.save(pic_io, format='PNG')
            signature = InMemoryUploadedFile(
                file=pic_io,
                field_name=None,
                name="%s.png" % pic.name.split('.')[0],
                content_type='image/png',
                size=getsizeof(pic_io),
                charset=None,
            )
        else:
            signature = ""
        form = Form.objects.get(id=request.data['form'])
        created_by = User.objects.get(id=request.data['created_by'])
        answer = Answer.objects.create(answer_text=answer_text, image=pic_file, signature=signature,
                                       form=form, created_by=created_by, unique_id=unique_id)
        question = Question.objects.get(id=request.data['question'])
        AnswerQuestion.objects.create(answers=answer, questions=question)
        return Response(request.data)


class AnswerDetailView(APIView):
    permission_classes = [ManagerPermission]

    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        answer = self.get_object(pk)
        form_equipment = FormEquipment.objects.get(forms=answer.form)
        equipment = Equipment.objects.get(id=form_equipment.equipments.id)
        answer_question = AnswerQuestion.objects.get(answers=answer)
        question = Question.objects.get(id=answer_question.questions.id)
        image = ""
        if answer.signature:
            signature = answer.signature.url
        else:
            signature = ""
        if answer.image:
            image = answer.image.url
        response = {
            "id": answer.id,
            "answer_text": answer.answer_text,
            "image": image,
            "signature": signature,
            "unique_id": answer.unique_id.id,
            "created_by": {
                "id": answer.created_by_id,
                "username": answer.created_by.username
            },
            "form_id": answer.form.id,
            "form_name": answer.form.form_name,
            "equipment_id": equipment.id,
            "equipment_code": equipment.equipment_code,
            "equipment_name": equipment.equipment_name.replace("_", " "),
            "room_id": equipment.room.id,
            "room_name": equipment.room.room_name.replace("_", " "),
            "room_location": equipment.room.location,
            "question_text": question.question_text,
            "is_active": answer.is_active,
            "created_at": answer.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return Response(response)

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
        return Response({"message": "record deleted"}, status=status.HTTP_204_NO_CONTENT)


class EquipmentToFromView(APIView):
    permission_classes = [ManagerPermission]

    def get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        equipment = self.get_object(pk)
        form_equipment = FormEquipment.objects.filter(equipments=equipment)
        equipment_arr = []
        for form_equipment in form_equipment:
            equipment_arr.append(
                {
                    "equipment_id": form_equipment.equipments.id,
                    "equipment_name": form_equipment.equipments.equipment_name,
                    "equipment_code": form_equipment.equipments.equipment_code,
                }
            )
        form_question = FormQuestion.objects.filter(forms=form_equipment.forms)
        question_arr = []
        for form_questions in form_question:
            question_arr.append(
                {
                    "question_id": form_questions.questions.id,
                    "question_text": form_questions.questions.question_text
                }
            )
        return Response(
            [
                {
                    "form_id": form_equipment.forms.id,
                    "form_name": form_equipment.forms.form_name,
                    "created_by_id": form_equipment.forms.created_by.id,
                    "created_by_name": form_equipment.forms.created_by.username,
                    "equipments": equipment_arr,
                    "questions": question_arr,
                    "is_active": form_equipment.forms.is_active
                }
            ]
        )


class RoomToFromView(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        room = self.get_object(pk)
        form_arr = []
        for equipment in Equipment.objects.filter(room=room):
            form_equipment = FormEquipment.objects.filter(equipments=equipment)
            for form_equipment in form_equipment:
                form_question = FormQuestion.objects.filter(forms=form_equipment.forms)
                question_arr = []
                for form_questions in form_question:
                    question_arr.append(
                        {
                            "question_id": form_questions.questions.id,
                            "question_text": form_questions.questions.question_text
                        }
                    )
                unique_id = UniqueId.objects.create();
                form_arr.append(
                    {
                        "form_id": form_equipment.forms.id,
                        "form_name": form_equipment.forms.form_name,
                        "unique_id": unique_id.id,
                        "created_by_id": form_equipment.forms.created_by.id,
                        "created_by_name": form_equipment.forms.created_by.username,
                        "equipments": [
                            {
                                "equipment_id": form_equipment.equipments.id,
                                "equipment_name": form_equipment.equipments.equipment_name,
                                "equipment_code": form_equipment.equipments.equipment_code,
                            }
                        ],
                        "questions": question_arr,
                        "is_active": form_equipment.forms.is_active
                    }
                )

        return Response(form_arr)


class ListReport(APIView):

    def get(self, request):
        lists = (Answer.objects.values('unique_id_id').annotate(dcount=Count('unique_id_id'))).order_by()
        i = []
        for l in lists:
            re = Answer.objects.filter(unique_id=l["unique_id_id"])[:1]
            for x in re:
                formEquipment = FormEquipment.objects.get(forms_id=x.form.id)
                i.append({
                    "unique_id": x.unique_id.id,
                    "room_id": formEquipment.equipments.room.id,
                    "room_name": formEquipment.equipments.room.room_name,
                })

        return Response(i)


class ExportPDFView(APIView):

    def get_object(self, pk):
        try:
            return UniqueId.objects.get(pk=pk)
        except UniqueId.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        unique_id = self.get_object(pk)
        answer_list = Answer.objects.filter(unique_id=unique_id)
        response = []
        for a in answer_list:
            formEquipment = FormEquipment.objects.get(forms_id=a.form.id)
            response.append(
                {
                    "room_id": formEquipment.equipments.room.id,
                    "room_name": formEquipment.equipments.room.room_name,
                    "use": a.created_at
                }
            )
        buffer = io.BytesIO()
        styles = getSampleStyleSheet()

        elements = []
        elements.append(Paragraph(
            "{}".format(
                answer_list[0].created_at.strftime("%Y-%m-%d")
            ), style=styles["Title"]
        ))
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph('Room Name (Location) : {}, {}'.format(FormEquipment.objects.get(
            forms_id=answer_list[0].form.id).equipments.room.room_name, FormEquipment.objects.get(
            forms_id=answer_list[0].form.id).equipments.room.location).replace("_", " "), style=styles["BodyText"]))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph('Inspector : {}'.format(answer_list[0].created_by)))
        if answer_list[0].image:
            image = platypus.Image(answer_list[0].image, width=150, height=150)
            elements.append(image)
        elements.append(Spacer(1, 0.2 * inch))
        data = [[None] * 4] * (answer_list.count() + 1)
        data[0] = ['Equipment Item', 'Normal', 'Defects', 'Follow Up Action']

        for a in range(0, answer_list.count()):
            formEquipment = FormEquipment.objects.get(forms_id=answer_list[a].form.id)
            answerQuestion = AnswerQuestion.objects.get(answers_id=answer_list[a].id)
            data[a + 1] = [formEquipment.equipments.equipment_name.replace("_", " "),
                           'Y' if answerQuestion.questions.question_text == "Normal ?" else " ",
                           'Y' if answerQuestion.questions.question_text == "Defects ?" else " ",
                           answerQuestion.answers.answer_text if answerQuestion.questions.question_text == "Follow up actions ?" else " "]
        table = Table(data, colWidths=100)
        table.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), .25, colors.black),
            ('BOX', (0, 0), (-1, -1), .25, colors.black),
            ('BACKGROUND', (0, 0), (-1, -len(data)), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(table)
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph("Signature"))
        elements.append(Spacer(1, 0.2 * inch))
        signature = platypus.Image(answer_list[0].signature, width=200, height=100)
        elements.append(signature)

        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm,
                                topMargin=1.5 * cm, bottomMargin=2.5 * cm, title="Form")
        doc.build(elements)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='{} Form.pdf'.format(
            FormEquipment.objects.get(forms_id=answer_list[0].form.id).equipments.room.room_name))

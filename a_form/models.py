import uuid

from django.db import models

from a_account.models import User

status = {
    (0, 'Inactive'),
    (1, 'Active')
}


class Room(models.Model):
    roomId = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    roomName = models.CharField(max_length=30)
    location = models.CharField(max_length=30)

    status = models.SmallIntegerField(choices=status, default=1)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.roomName


class Question(models.Model):
    questionId = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    questionText = models.CharField(max_length=30)

    status = models.SmallIntegerField(choices=status, default=1)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.questionText


class Equipment(models.Model):
    equipmentId = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    equipmentName = models.CharField(max_length=30)
    equipmentCode = models.CharField(max_length=30, blank=True, null=True)
    room = models.ForeignKey(Room, related_name='equipments', on_delete=models.CASCADE)
    ThisInspectionOn = models.DateTimeField(auto_now=True)
    NextInspectionOn = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(choices=status, default=1)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.equipmentName


class Form(models.Model):
    formId = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    formName = models.CharField(max_length=30, verbose_name="Form Name", blank=False)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Created By")

    equipments = models.ManyToManyField(Equipment, through='FormEquipment')
    questions = models.ManyToManyField(Question, through='FormQuestion')

    status = models.SmallIntegerField(choices=status, default=1)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.formName


class FormEquipment(models.Model):
    form = models.ForeignKey(Form, related_name='forms', on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, related_name='equipments', on_delete=models.CASCADE)


class FormQuestion(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Answer(models.Model):
    answerId = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    answer = models.CharField(max_length=30)

    form = models.ForeignKey(Form, on_delete=models.CASCADE, verbose_name="Form")
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Created By")
    question = models.ManyToManyField(Question)

    status = models.SmallIntegerField(choices=status, default=1)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer


class AnswerQuestion(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

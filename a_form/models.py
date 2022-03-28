import os
import uuid
from django.db import models
from a_account.models import User


class Room(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    room_name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room_name


class Question(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    question_text = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text


class Equipment(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    equipment_name = models.CharField(max_length=30)
    equipment_code = models.CharField(max_length=30, blank=True, null=True)

    room = models.ForeignKey(Room, related_name='equipments', on_delete=models.CASCADE)

    this_inspection_on = models.DateTimeField(auto_now=True)
    next_inspection_on = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.equipment_name


class Form(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    form_name = models.CharField(max_length=30, verbose_name="Form Name", blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Created By")

    equipments = models.ManyToManyField(Equipment, through='FormEquipment')
    questions = models.ManyToManyField(Question, through='FormQuestion')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.form_name


class FormEquipment(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    forms = models.ForeignKey(Form, related_name='forms', on_delete=models.CASCADE)
    equipments = models.ForeignKey(Equipment, related_name='equipments', on_delete=models.CASCADE)


class FormQuestion(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    forms = models.ForeignKey(Form, on_delete=models.CASCADE)
    questions = models.ForeignKey(Question, on_delete=models.CASCADE)


def path_and_rename(instance, filename):
    upload_to = 'image/record/%Y%m%d'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid.uuid4())
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    answer_text = models.CharField(max_length=30, null=True, blank=True)

    form = models.ForeignKey(Form, on_delete=models.CASCADE, verbose_name="Form")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Created By")
    image = models.ImageField(upload_to=path_and_rename, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer_text


class AnswerQuestion(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    answers = models.ForeignKey(Answer, on_delete=models.CASCADE)
    questions = models.ForeignKey(Question, on_delete=models.CASCADE)

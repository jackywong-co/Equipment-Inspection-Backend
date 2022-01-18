from django.contrib import admin

from .models import *

admin.site.register(Room)
admin.site.register(Equipment)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(FormEquipment)
admin.site.register(FormQuestion)
admin.site.register(AnswerQuestion)


# Form Creation
class FormQuestionInline(admin.TabularInline):
    model = FormQuestion
    extra = 0


class FormEquipmentInline(admin.TabularInline):
    model = FormEquipment
    extra = 0


@admin.register(Form)
class Form(admin.ModelAdmin):
    fields = ('formName', 'createdBy', 'status')
    inlines = [FormEquipmentInline, FormQuestionInline]

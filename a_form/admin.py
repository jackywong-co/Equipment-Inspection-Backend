from django.contrib import admin

# Register your models here.
from a_form.models import Room, Equipment


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin

# Register your models here.
from a_form.models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass
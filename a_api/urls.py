from django.urls import path
from a_api.views import RoomView, RoomDetailView, EquipmentView

urlpatterns = [
    path('room/', RoomView.as_view()),
    path('room/<str:pk>', RoomDetailView.as_view()),
    path('equipment/', EquipmentView.as_view()),
]

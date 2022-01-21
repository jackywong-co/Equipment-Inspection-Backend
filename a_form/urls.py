from django.urls import path
from a_form.views import RoomView, RoomDetailView, EquipmentView,EquipmentDetailView, UserView, FormView

urlpatterns = [

    path('user/', UserView.as_view()),
    path('room/', RoomView.as_view()),
    path('room/<str:pk>', RoomDetailView.as_view()),
    path('equipment/', EquipmentView.as_view()),
    path('equipment/<str:pk>', EquipmentDetailView.as_view()),
    path('form/', FormView.as_view()),

]

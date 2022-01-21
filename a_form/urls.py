from django.urls import path, include
from a_form.views import RoomView, RoomDetailView, EquipmentView, UserView, FormView


urlpatterns = [

    path('user/', UserView.as_view()),
    path('room/', RoomView.as_view()),
    path('room/<str:pk>', RoomDetailView.as_view()),
    path('equipment/', EquipmentView.as_view()),

    path('form/', FormView.as_view()),
    # path('', SignInView.as_view(), name='home'),
    # path('dashboard/', DashboardView.as_view(), name='dashboard')
]

from django.urls import path
from a_form.views import RoomView, RoomDetailView, EquipmentView, EquipmentDetailView, UserView, FormView, QuestionView, \
    FormEquipmentView, FormDetailView, FormQuestionView, FormEquipmentDetailView, FormQuestionDetailView

urlpatterns = [

    path('user/', UserView.as_view()),

    path('room/', RoomView.as_view()),
    path('room/<str:pk>', RoomDetailView.as_view()),

    path('equipment/', EquipmentView.as_view()),
    path('equipment/<str:pk>', EquipmentDetailView.as_view()),

    path('form/', FormView.as_view()),
    path('form/<str:pk>/', FormDetailView.as_view()),

    path('question/', QuestionView.as_view()),

    path('formEquipmentView/', FormEquipmentView.as_view()),
    path('formEquipmentView/<str:pk>/', FormEquipmentDetailView.as_view()),

    path('formQuestionView/', FormQuestionView.as_view()),
    path('formEquipmentView/<str:pk>/', FormQuestionDetailView.as_view()),

]

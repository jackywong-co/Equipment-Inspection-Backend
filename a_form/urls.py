from django.urls import path
from a_form.views import (UserView, UserDetailView,
                          RoomView, RoomDetailView,
                          EquipmentView, EquipmentDetailView,
                          FormView, FormDetailView,
                          QuestionView,
                          FormEquipmentView,
                          FormQuestionView,
                          FormEquipmentDetailView,
                          FormQuestionDetailView,
                          AnswerView, QuestionDetailView, AnswerDetailView, EquipmentImageView, EquipmentToFromView,
                          RoomToFromView
                          )

urlpatterns = [

    path('user/', UserView.as_view()),
    path('user/<str:pk>/', UserDetailView.as_view()),

    path('room/', RoomView.as_view()),
    path('room/<str:pk>/', RoomDetailView.as_view()),

    path('equipment/', EquipmentView.as_view()),
    path('equipment/<str:pk>/', EquipmentDetailView.as_view()),
    path('equipmentImage/', EquipmentImageView.as_view()),

    path('form/', FormView.as_view()),
    path('form/<str:pk>/', FormDetailView.as_view()),

    path('question/', QuestionView.as_view()),
    path('question/<str:pk>/', QuestionDetailView.as_view()),

    path('answer/', AnswerView.as_view()),
    path('answer/<str:pk>/', AnswerDetailView.as_view()),

    path('formEquipmentView/', FormEquipmentView.as_view()),
    path('formEquipmentView/<str:pk>/', FormEquipmentDetailView.as_view()),

    path('formQuestionView/', FormQuestionView.as_view()),
    path('formEquipmentView/<str:pk>/', FormQuestionDetailView.as_view()),

    path('equipmentToForm/<str:pk>/', EquipmentToFromView.as_view()),
    path('roomToForm/<str:pk>/', RoomToFromView.as_view()),
]

from django.urls import path

from a_classifier.views import TrainingView, PredictView

urlpatterns = [
    path('training/', TrainingView.as_view()),
    path('predict/', PredictView.as_view()),
]

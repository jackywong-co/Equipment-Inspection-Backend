from django.urls import path

from a_classifier.views import TrainingView

urlpatterns = [
    path('training/', TrainingView.as_view()),
]

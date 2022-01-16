from django.urls import path, include
from a_form.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home')
]
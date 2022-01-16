from django.urls import path, include
from a_form.views import SignInView

urlpatterns = [
    path('', SignInView.as_view(), name='home')
]
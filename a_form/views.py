from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class SignInView(TemplateView):
    template_name = "login.html"

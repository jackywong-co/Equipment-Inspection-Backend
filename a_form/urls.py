from django.urls import path, include
from a_form.views import SignInView, DashboardView

urlpatterns = [
    path('', SignInView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard')
]

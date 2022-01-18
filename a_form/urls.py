from django.urls import path, include
<<<<<<< HEAD
from a_form.views import SignInView, DashboardView

urlpatterns = [
    path('', SignInView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard')
]
=======
from a_form.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home')
]
>>>>>>> parent of 148b667 (jwt)

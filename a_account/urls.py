from django.urls import path
from a_account.views import RegisterView, LogoutView, LoginView, RefreshView, VerifyView

urlpatterns = [

    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', RefreshView.as_view(), name='token_refresh'),
    path('verify/', VerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(), name="logout"),

]

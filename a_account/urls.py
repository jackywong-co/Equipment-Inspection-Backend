from django.urls import path
from a_account.views import RegisterView, LoginView, UserView,LogoutView

urlpatterns = [

    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('user/', UserView.as_view(), name="authenticated"),
path('logout/', LogoutView.as_view(), name="logout"),

]

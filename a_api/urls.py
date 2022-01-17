from django.urls import path
from a_account.views import LoginView, RegisterView
from a_api.views import RoomView, RoomDetailView, EquipmentView, UserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [

    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('user/', UserView.as_view()),
    path('room/', RoomView.as_view()),
    path('room/<str:pk>', RoomDetailView.as_view()),
    path('equipment/', EquipmentView.as_view()),
    # path('test/', ExampleView.as_view()),

    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

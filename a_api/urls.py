
from django.urls import path, include

from a_form.views import RoomView, RoomDetailView, EquipmentView, UserView, FormView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('auth/', include('a_account.urls')),

    path('user/', UserView.as_view()),
    path('room/', RoomView.as_view()),
    path('room/<str:pk>', RoomDetailView.as_view()),
    path('equipment/', EquipmentView.as_view()),

    path('form/', FormView.as_view()),
    # path('test/', ExampleView.as_view()),

    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

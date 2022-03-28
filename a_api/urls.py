from django.urls import path, include

urlpatterns = [
    path('', include('a_account.urls')),
    path('', include('a_form.urls')),
    path('', include('a_classifier.urls')),
]

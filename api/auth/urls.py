from api.auth.views import AccountRegisterViewSet
from django.urls import path


urlpatterns = [
    path('register/', AccountRegisterViewSet.as_view(), name='auth_register')
]

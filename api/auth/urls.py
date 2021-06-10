from api.auth.views import AccountRegisterViewSet
from rest_framework.authtoken import views
from django.urls import path


urlpatterns = [
    path('register/', AccountRegisterViewSet.as_view(), name='auth_register'),
    path('token/', views.obtain_auth_token)
]

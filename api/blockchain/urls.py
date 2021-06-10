from django.urls import include, path
from rest_framework import routers
from api.blockchain import views

router = routers.DefaultRouter()
router.register(r'coins', views.CoinViewSet)
router.register(r'accounts', views.AccountViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('accounts/<int:pk>/wallets/<int:wallet_id>/', views.AccountViewSet.as_view({"put": "wallets"})),
    path('accounts/<int:pk>/wallets/<int:wallet_id>/transactions', views.AccountViewSet.as_view({"get": "transactions", "post": "transactions"}))
]

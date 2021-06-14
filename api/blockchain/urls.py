from django.urls import include, path
from rest_framework import routers
from api.blockchain import views

router = routers.DefaultRouter()
router.register(r'coins', views.CoinViewSet)
router.register(r'wallets', views.WalletViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('wallets/<int:pk>/transactions', views.WalletViewSet.as_view({"get": "transactions", "post": "transactions"}))
]

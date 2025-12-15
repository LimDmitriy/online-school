from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import PaymentViewSet, UserCreateAPIView, UserViewSet

from .apps import UsersConfig

app_name = UsersConfig.name

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("payments", PaymentViewSet)

urlpatterns = [
    path("registration/", UserCreateAPIView.as_view(), name="registration"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]

urlpatterns += router.urls

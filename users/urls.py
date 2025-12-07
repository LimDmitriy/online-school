from rest_framework.routers import SimpleRouter

from users.views import PaymentViewSet, UserViewSet

from .apps import UsersConfig

app_name = UsersConfig.name

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("payments", PaymentViewSet)

urlpatterns = []

urlpatterns += router.urls

from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class UserSerializer(ModelSerializer):
    """Сериализатор пользователей"""

    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    """Сериализатор платежей"""

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("user", "session_id", "link")

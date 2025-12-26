from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import (
    convert_rub_to_dollars,
    create_stripe_price,
    create_stripe_session,
)


class UserViewSet(ModelViewSet):
    """Контроллер пользователей"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentViewSet(ModelViewSet):
    """Контроллер платежей"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "date",
        "course",
        "lesson",
        "payment_method",
    ]
    ordering_fields = ["date"]
    ordering = ["date"]


class UserCreateAPIView(CreateAPIView):
    """Контроллер регистрации пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentCreateAPIView(CreateAPIView):
    """Контроллер регистрации пользователя"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_in_dollar = convert_rub_to_dollars(payment.amount)
        price = create_stripe_price(amount_in_dollar)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

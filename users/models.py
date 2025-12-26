from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Укажите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счёт"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    date = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный курс",
        blank=True,
        null=True,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный урок",
        blank=True,
        null=True,
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="id сессии",
        help_text="Укажите id",
    )
    link = models.URLField(
        max_length=2000,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.payment_method})"

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

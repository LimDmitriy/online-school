from rest_framework.serializers import ValidationError


class UrlValidator:
    """Вагинатор для проверки ссылки уроков и курсов"""

    def __call__(self, value):
        if "youtube.com" not in value:
            raise ValidationError(f"Разрешены ссылки только на youtube.com")

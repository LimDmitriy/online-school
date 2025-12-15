from django.db import models


class Course(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    image = models.ImageField(
        upload_to="materials/images/course",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Добавьте превью курса",
    )
    descriptions = models.TextField(
        verbose_name="Описание", help_text="Введите описание курса"
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца",
    )

    def __str__(self):
        return f"{self.title} - {self.descriptions}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    image = models.ImageField(
        upload_to="materials/images/lesson",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Добавьте превью урока",
    )
    descriptions = models.TextField(
        verbose_name="Описание", help_text="Введите описание урока"
    )
    url = models.CharField(
        max_length=150, verbose_name="Ссылка", help_text="Укажите ссылку"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
        help_text="Укажите курс, к которому относится урок",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

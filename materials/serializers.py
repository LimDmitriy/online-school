from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import UrlValidator


class LessonSerializer(ModelSerializer):
    url = serializers.URLField(
        validators=[UrlValidator()], required=False, allow_null=True
    )

    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ("owner",)


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_lesson_count(self, course):
        return course.lessons.count()

    def get_is_subscribed(self, course):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return False

        return Subscription.objects.filter(user=request.user, course=course).exists()

    class Meta:
        model = Course
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"

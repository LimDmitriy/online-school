from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import UrlValidator


class LessonSerializer(ModelSerializer):
    url = serializers.URLField(validators=[UrlValidator()])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    url = serializers.URLField(validators=[UrlValidator()])
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"

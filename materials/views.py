from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.permissions import IsModerator, IsOwnerOrModerator
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)
from materials.tasks import send_course_update_email


class CourseViewSet(ModelViewSet):
    """CRUD вьюсет, контроллер курсов"""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsModerator, IsOwnerOrModerator]
    pagination_class = CustomPagination

    def perform_update(self, serializer):
        course = serializer.save()
        send_course_update_email.delay(course.id)


class LessonCreateApiView(CreateAPIView):
    """Коньтроллер для создания уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonListApiView(ListAPIView):
    """Контроллер для просмотра всех уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all().order_by("id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class LessonRetriveApiView(RetrieveAPIView):
    """Контроллер для детального просмотра урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonUpdateApiView(UpdateAPIView):
    """Контроллер для обновления урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def perform_update(self, serializer):
        lesson = serializer.save()
        send_course_update_email.delay(lesson.course.id)


class LessonDestroyApiView(DestroyAPIView):
    """Контроллер для удаления урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class SubscriptionAPIView(APIView):
    """Контроллер для добавления и удаления подписки"""

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})

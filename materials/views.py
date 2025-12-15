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
from materials.permissions import IsModerator, IsOwnerOrModerator
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)


class CourseViewSet(ModelViewSet):
    """CRUD вьюсет, контроллер курсов"""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsModerator, IsOwnerOrModerator]


class LessonCreateApiView(CreateAPIView):
    """Коньтроллер для создания уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonListApiView(ListAPIView):
    """Контроллер для просмотра всех уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


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

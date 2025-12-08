from django.http import HttpRequest, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView
)
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from test_app.serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskDetailSerializer,
)
from test_app.models import Task
from test_app.permissions import IsAuthenticatedForModification, IsOwnerOrReadOnly
from django.db.models import Count


WEEK_DAY_MAP = {
    "sunday": 1,
    "monday": 2,
    "tuesday": 3,
    "wednesday": 4,
    "thursday": 5,
    "friday": 6,
    "saturday": 7
}


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']     # (/?status=, /?deadline=) Фильтрация по статусу и дедлайну
    search_fields = ['title', 'description']      # (/?search= ) Поиск по заголовку и описанию
    ordering_fields = ['created_at']              # (/?ordering= ) Сортировка по дате создания
    ordering = ['-created_at']                    # Сортировка по умолчанию

    # ПЕРМИШЕНЫ: Чтение всем, создание только авторизованным
    permission_classes = [IsAuthenticatedForModification]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskListSerializer


    def get_queryset(self):
        queryset = super().get_queryset()
        week_day = self.request.query_params.get('week_day', '').lower().strip()
        if week_day and (week_day_num := WEEK_DAY_MAP.get(week_day)):
            queryset = queryset.filter(deadline__week_day=week_day_num)

        return queryset


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            self.perform_create(serializer)
        except Exception as exc:
            return Response(
                data={
                    "error": "Ошибка сохранения задачи",
                    "detail": str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    lookup_field = 'id'

    # ПЕРМИШЕНЫ: Только авторизованные
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskCreateSerializer
        return TaskDetailSerializer


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            self.perform_update(serializer)
        except Exception as exc:
            return Response(
                data={
                    "error": "Ошибка обновления задачи",
                    "detail": str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            self.perform_destroy(instance)
        except Exception as exc:
            return Response(
                data={
                    "error": "Ошибка удаления задачи",
                    "detail": str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(data={}, status=status.HTTP_204_NO_CONTENT)


class MyTasksView(ListAPIView):
    """
    Получить задачи текущего пользователя.
    """
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'deadline']
    ordering = ['-created_at']

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)




@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Только авторизованные
def get_tasks_statistics(request):
    total_tasks = Task.objects.count()

    tasks_by_status = (Task.objects
                       .values('status')
                       .annotate(count=Count('id')))

    overdue_tasks = Task.objects.filter(
        deadline__lt=datetime.now().date()
    ).exclude(status='Done').count()

    statistics = {
        'total_tasks': total_tasks,
        'tasks_by_status': list(tasks_by_status),
        'overdue_tasks': overdue_tasks
    }

    return Response(
        data=statistics,
        status=status.HTTP_200_OK
    )


def home_page(request: HttpRequest):
    return HttpResponse(f"""
        <h1 style="color: #008080;">Hello, Guest!</h1>
    """)

def user_page(request: HttpRequest, user_name):
    return HttpResponse(f"""
        <h1 style="color: #008080;">We are glad to see you, {user_name}!</h1>
    """)
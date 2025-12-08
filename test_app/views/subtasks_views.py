from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from test_app.models import SubTask, Task
from test_app.serializers import SubTaskCreateSerializer, SubTaskSerializer
from test_app.permissions import IsOwnerOrReadOnly


class SubTaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'pagination': {
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'total_count': self.page.paginator.count,
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
                'page_size': self.get_page_size(self.request)
            }
        })


class SubTaskListCreateView(ListCreateAPIView):
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # Фильтр через query params: ?status=, ?deadline=
    filterset_fields = ['status', 'deadline']

    # Поиск ?search= (ищет в title, description )
    search_fields = ['title', 'description']

    # Сортировка ?ordering=created_at или ?ordering=-created_at
    ordering_fields = ['created_at']
    ordering = ['-created_at']                  # по умолчанию


    def get_queryset(self):
        queryset = SubTask.objects.all()
        task_id = self.kwargs.get('task_id')
        if task_id:
            queryset = queryset.filter(task_id=task_id)
        return queryset


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer


    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(id=task_id)
        serializer.save(task=task, owner=self.request.user)


    def create(self, request, *args, **kwargs):
        task_id = self.kwargs.get('task_id')

        if not task_id:
            return Response(
                data={
                    "error": "Для создания подзадачи используйте URL формат: /api/tasks/1/subtasks/"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                data={"error": f"Задача с id {task_id} не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            self.perform_create(serializer)
            subtask = serializer.instance
        except Exception as exc:
            return Response(
                data={
                    "error": "Ошибка сохранения подзадачи",
                    "detail": str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            data=SubTaskSerializer(subtask).data,
            status=status.HTTP_201_CREATED
        )


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    lookup_field = 'id'

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SubTaskCreateSerializer
        return SubTaskSerializer


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.perform_update(serializer)
        except Exception as exc:
            return Response(
                data={"error": f"Ошибка при обновлении подзадачи: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            self.perform_destroy(instance)
        except Exception as exc:
            return Response(
                data={"error": f"Ошибка при удалении подзадачи: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(data={}, status=status.HTTP_204_NO_CONTENT)

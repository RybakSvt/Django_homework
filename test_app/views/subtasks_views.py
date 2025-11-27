from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from test_app.models import SubTask, Task
from test_app.serializers import (
    SubTaskCreateSerializer,
    SubTaskSerializer,
)

from django.core.paginator import Paginator, EmptyPage


class SubTaskListCreateView(APIView):
    DEFAULT_PAGE_SIZE = 5
    MAX_PAGE_SIZE = 100


    def get_queryset(self, request, task_id: int = None):
        queryset = SubTask.objects.all()
        if task_id:
            queryset = queryset.filter(task_id=task_id)
        task_title = request.query_params.get('task_title')
        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)
        status = request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('-created_at')


    def _get_validated_int_param(self, request, param_name, default, min_value=1, max_value=None):
        param_value = request.query_params.get(param_name, default)
        try:
            value = int(param_value)
            value = max(value, min_value)
            if max_value:
                value = min(value, max_value)
            return value
        except (TypeError, ValueError):
            return default


    def get_pagination_params(self, request):
        page_size = self._get_validated_int_param(
            request, 'page_size', self.DEFAULT_PAGE_SIZE,
            min_value=1, max_value=self.MAX_PAGE_SIZE
        )
        page = self._get_validated_int_param(request, 'page', 1, min_value=1)
        return page, page_size


    def get_paginated_response(self, paginator, page_obj, serializer_data, page_size):
        return Response({
            'data': serializer_data,
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'page_size': page_size
            }
        }, status=status.HTTP_200_OK)


    def get(self, request: Request, task_id: int = None) -> Response:
        try:
            subtasks = self.get_queryset(request, task_id)
            page, page_size = self.get_pagination_params(request)
            paginator = Paginator(subtasks, page_size)
            try:
                subtasks_page = paginator.page(page)
            except EmptyPage:
                return Response(
                    data={"error": "Страница не найдена"},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = SubTaskSerializer(subtasks_page, many=True)
            return self.get_paginated_response(paginator, subtasks_page, serializer.data, page_size)
        except Exception as exc:
            return Response(
                data={"error": "Внутренняя ошибка сервера"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    def post(self, request: Request, task_id: int = None) -> Response:
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

        serializer = SubTaskCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            subtask = serializer.save(task=task)
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

class SubTaskDetailUpdateDeleteView(APIView):


    def get_object(self, subtask_id: int):
        try:
            return SubTask.objects.get(pk=subtask_id)
        except SubTask.DoesNotExist:
            return None


    def get(self, request: Request, subtask_id: int) -> Response:
        subtask = self.get_object(subtask_id)
        if not subtask:
            return Response(
                data={"error": f"Подзадача с id={subtask_id} не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        subtask_dto = SubTaskSerializer(subtask)
        return Response(data=subtask_dto.data, status=status.HTTP_200_OK)


    def put(self, request: Request, subtask_id: int) -> Response:
        subtask = self.get_object(subtask_id)
        if not subtask:
            return Response(
                data={"error": f"Подзадача с id={subtask_id} не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        subtask_dto = SubTaskSerializer(instance=subtask, data=request.data)
        if not subtask_dto.is_valid():
            return Response(data=subtask_dto.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            subtask_dto.save()
        except Exception as exc:
            return Response(
                data={"error": f"Ошибка при обновлении подзадачи: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(data=subtask_dto.data, status=status.HTTP_200_OK)


    def patch(self, request: Request, subtask_id: int) -> Response:
        subtask = self.get_object(subtask_id)
        if not subtask:
            return Response(
                data={"error": f"Подзадача с id={subtask_id} не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        subtask_dto = SubTaskSerializer(instance=subtask, data=request.data, partial=True)
        if not subtask_dto.is_valid():
            return Response(
                data=subtask_dto.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            subtask_dto.save()
        except Exception as exc:
            return Response(
                data={"error": f"Ошибка при обновлении подзадачи: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(data=subtask_dto.data, status=status.HTTP_200_OK)


    def delete(self, request: Request, subtask_id: int) -> Response:
        subtask = self.get_object(subtask_id)
        if not subtask:
            return Response(
                data={"error": f"Подзадача с id={subtask_id} не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            subtask.delete()
        except Exception as exc:
            return Response(
                data={"error": f"Ошибка при удалении подзадачи: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            data={},
            status=status.HTTP_204_NO_CONTENT
        )


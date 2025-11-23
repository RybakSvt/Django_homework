from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from test_app.models import SubTask, Task
from test_app.serializers import (
    SubTaskCreateSerializer,
    SubTaskSerializer,
)


class SubTaskListCreateView(APIView):

    def get(self, request: Request, task_id: int = None)-> Response:
        if task_id:
            subtasks = SubTask.objects.filter(task_id=task_id)
        else:
            subtasks = SubTask.objects.all()

        subtasks_dto = SubTaskSerializer(subtasks, many=True)
        return Response(
            data=subtasks_dto.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request, task_id: int = None)-> Response:
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

        subtasks_dto = SubTaskCreateSerializer(data=request.data)
        if not subtasks_dto.is_valid():
            return Response(
                data=subtasks_dto.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            subtask = subtasks_dto.save(task=task)
        except Exception as exc:
            return Response(
                data={
                    "error": f"Ошибка сохранения подзадачи",
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


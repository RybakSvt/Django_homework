from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view
from test_app.serializers import TaskCreateSerializer
from test_app.serializers import TaskListSerializer
from test_app.serializers import TaskDetailSerializer
from test_app.models import Task
from django.db.models import Count, Q
from datetime import datetime


@api_view(['GET',])
def get_all_tasks(request: Request) -> Response:
    tasks = Task.objects.all()
    tasks_dto = TaskListSerializer(tasks, many=True)
    return Response(
        data=tasks_dto.data,
        status=status.HTTP_200_OK
    )


@api_view(['GET',])
def get_task_by_id(request: Request, task_id: int) -> Response:
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return Response(
            data={"error": f"Задачи с id={task_id} в базе не найдено"},
            status=status.HTTP_404_NOT_FOUND
        )

    task_dto =TaskDetailSerializer(task)
    return Response(
        data=task_dto.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST',])
def create_new_task(request: Request) -> Response:
    task_dto = TaskCreateSerializer(data=request.data)
    if not task_dto.is_valid():
        return Response(
            data=task_dto.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        task_dto.save()
    except Exception as exc:
        return Response(
            data = {
                "error": f"Ошибка сохранения задачи",
                "detail": str(exc)
                    },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return Response(
        data=task_dto.data,
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
def get_tasks_statistics(request: Request) -> Response:

    total_tasks = Task.objects.count()

    tasks_by_status = (Task.objects
                       .values('status')
                       .annotate(count=Count('id')))

    overdue_tasks = Task.objects.filter(
        deadline__lt=datetime.now().date()
    ).count()

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
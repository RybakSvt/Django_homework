from django.urls import path
from test_app.views import (
    TaskListCreateView,
    TaskDetailUpdateDeleteView,
    get_tasks_statistics,
    SubTaskListCreateView,
)

urlpatterns = [
    path('', TaskListCreateView.as_view()),
    path('<int:id>/', TaskDetailUpdateDeleteView.as_view()),
    path('statistics/', get_tasks_statistics),
    path('<int:task_id>/subtasks/', SubTaskListCreateView.as_view()),
]
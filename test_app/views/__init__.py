__all__ = [
    'TaskListCreateView',
    'TaskDetailUpdateDeleteView',
    'get_tasks_statistics',
    'home_page',
    'user_page',
    'SubTaskListCreateView',
    'SubTaskDetailUpdateDeleteView',
    'CategoryViewSet',
    'MyTasksView',
]

from .task_views import (
    TaskListCreateView,
    TaskDetailUpdateDeleteView,
    MyTasksView,
    get_tasks_statistics,
    home_page,
    user_page,
)

from .subtasks_views import (
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)

from .categories_views import (
    CategoryViewSet
)

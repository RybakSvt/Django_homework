__all__ = [
    'TaskListCreateView',
    'TaskDetailUpdateDeleteView',
    'get_tasks_statistics',
    'home_page',
    'user_page',
    'SubTaskListCreateView',
    'SubTaskDetailUpdateDeleteView',
    'CategoryListCreateView',
    'CategoryDetailUpdateDeleteView',
]

from .task_views import (
    TaskListCreateView,
    TaskDetailUpdateDeleteView,
    get_tasks_statistics,
    home_page,
    user_page,
)

from .subtasks_views import (
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)

from .categories_views import (
    CategoryListCreateView,
    CategoryDetailUpdateDeleteView,
)



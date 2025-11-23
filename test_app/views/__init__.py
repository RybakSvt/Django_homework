__all__ = [
    'get_all_tasks',
    'get_task_by_id',
    'create_new_task',
    'get_tasks_statistics',
    'home_page',
    'user_page',
    'SubTaskListCreateView',
    'SubTaskDetailUpdateDeleteView',
    'CategoryListCreateView',
    'CategoryDetailUpdateDeleteView',
]

from .task_views import (
    get_all_tasks,
    get_task_by_id,
    create_new_task,
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
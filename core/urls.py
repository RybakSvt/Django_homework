"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from test_app.views import home_page, user_page
from test_app.views import create_new_task
from test_app.views import get_all_tasks
from test_app.views import get_task_by_id
from test_app.views import get_tasks_statistics

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),                       # Домашняя страница
    path('user/<str:user_name>/', user_page),  # Страница пользователя
    path('api/v1/tasks/', get_all_tasks),
    path('api/v1/tasks/<int:task_id>/',get_task_by_id),
    path('api/v1/tasks/create/', create_new_task),
    path('api/v1/tasks/statistics/', get_tasks_statistics),

]

from django.urls import path, include


urlpatterns = [
    path('tasks/', include('test_app.urls.tasks')),
    path ('subtasks/', include('test_app.urls.subtasks')),
    path('categories/', include('test_app.urls.categories')),
]
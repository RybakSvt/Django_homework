from django.urls import path, include
from rest_framework.routers import DefaultRouter
from test_app.views.categories_views import CategoryViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('tasks/', include('test_app.urls.tasks')),
    path('subtasks/', include('test_app.urls.subtasks')),
] + router.urls

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from test_app.views.auth import RegisterView, LoginView, LogoutView

from test_app.views.categories_views import CategoryViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('tasks/', include('test_app.urls.tasks')),
    path('subtasks/', include('test_app.urls.subtasks')),
    path('jwt-auth/', TokenObtainPairView.as_view()),
    path('jwt-refresh/', TokenRefreshView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),  # кастомный логин с cookies
    path('logout/', LogoutView.as_view()),

] + router.urls

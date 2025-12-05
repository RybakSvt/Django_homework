from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from test_app.models import Category
from test_app.serializers import CategorySerializer, CategoryCreateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с категориями.
    Поддерживает мягкое удаление и полное удаление (только для админов).
    """
    queryset = Category.objects.all()  # Использует наш менеджер - покажет только неудалённые
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CategoryCreateSerializer
        return CategorySerializer

    def destroy(self, request, *args, **kwargs):
        """
        Переопределяем удаление для мягкого удаления.
        Вместо реального удаления из БД помечаем как удалённое.
        """
        instance = self.get_object()

        # Мягкое удаление
        instance.soft_delete()

        return Response(
            {
                'message': f'Категория "{instance.name}" помечена как удалённая',
                'deleted_at': instance.deleted_at
            },
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'])
    def deleted(self, request):
        """Получить список удалённых категорий"""
        deleted_categories = Category.objects.deleted()
        serializer = CategorySerializer(deleted_categories, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Восстановить удалённую категорию"""
        category = Category.objects.all_with_deleted().get(pk=pk, is_deleted=True)
        category.restore()

        return Response(
            {
                'message': f'Категория "{category.name}" восстановлена',
                'restored_at': timezone.now()
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['delete'], permission_classes=[IsAdminUser])
    def hard_delete(self, request, pk=None):
        """
        Полное удаление категории из базы данных.
        Доступно только администраторам.
        """
        category = Category.objects.all_with_deleted().get(pk=pk)

        # Полное удаление
        category.delete(hard=True)

        return Response(
            {
                'message': f'Категория "{category.name}" полностью удалена из базы данных',
                'deleted_completely': True
            },
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        """Подсчёт задач в категории (только для неудалённых категорий)"""
        category = self.get_object()
        tasks_count = category.task_set.count()

        return Response({
            'category_id': category.id,
            'category_name': category.name,
            'tasks_count': tasks_count,
            'is_deleted': category.is_deleted
        }, status=status.HTTP_200_OK)
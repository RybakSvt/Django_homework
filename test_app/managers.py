from django.db import models


class CategoryManager(models.Manager):
    """
    Кастомный менеджер для модели Category.
    По умолчанию возвращает только неудалённые категории.
    """


    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


    def deleted(self):
        """Возвращает только удалённые категории"""
        return super().get_queryset().filter(is_deleted=True)


    def all_with_deleted(self):
        """Возвращает все категории (включая удалённые)"""
        return super().get_queryset().all()


    def hard_delete(self):
        """Полное удаление категорий из базы данных"""
        return super().get_queryset().delete()
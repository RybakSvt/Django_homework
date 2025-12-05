from django.db import models
from django.utils import timezone
from .managers import CategoryManager


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    # Поля для мягкого удаления
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата удаления")


    objects = CategoryManager()  # Кастомный менеджер По умолчанию показывает только неудалённые


    def __str__(self):
        return self.name


    def soft_delete(self):
        """Метод мягкого удаления"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

        # import logging
        # logger = logging.getLogger(__name__)
        # logger.info(f"Категория '{self.name}' помечена как удалённая")


    def restore(self):
        """Восстановление из удалённых"""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at'])

        # import logging
        # logger = logging.getLogger(__name__)
        # logger.info(f"Категория '{self.name}' восстановлена")


    def delete(self, *args, **kwargs):
        """Переопределение стандартного удаления с поддержкой hard delete"""
        if kwargs.pop('hard', False):

            # import logging
            # logger = logging.getLogger(__name__)
            # logger.info(f"Категория '{self.name}' полностью удалена из БД")
            super().delete(*args, **kwargs)
        else:  # мягкое удаление по умолчанию
            self.soft_delete()


    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200, unique=True, verbose_name="Название задачи")
    description = models.TextField(blank=True, verbose_name="Описание задачи")
    categories = models.ManyToManyField(Category, blank=True, verbose_name="Категории задачи")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус задачи"
    )
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class SubTask(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200, unique=True, verbose_name="Название подзадачи")
    description = models.TextField(blank=True, verbose_name="Описание подзадачи")
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='subtasks',
        verbose_name="Основная задача"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус подзадачи"
    )
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
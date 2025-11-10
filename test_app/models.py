from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название категории")


class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название задачи")
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


class SubTask(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название подзадачи")
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

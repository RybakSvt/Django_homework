import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from datetime import timedelta
from django.utils import timezone
from test_app.models import Task, SubTask
from django.db.models import Q

# Создание записей:
#
# Task:
#     title: "Prepare presentation".
#     description: "Prepare materials and slides for the presentation".
#     status: "New".
#     deadline: Today's date + 3 days.
# SubTasks для "Prepare presentation":
# title: "Gather information".
#     description: "Find necessary information for the presentation".
#     status: "New".
#     deadline: Today's date + 2 days.
# title: "Create slides".
#     description: "Create presentation slides".
#     status: "New".
#     deadline: Today's date + 1 day.


# task_deadline = timezone.now() + timedelta(days=3)
# task_new = Task.objects.create(
#     title="Prepare presentation",
#     description="Prepare materials and slides for the presentation",
#     status="New",
#     deadline=task_deadline
# )
# print(f"Создана задача: {task_new.title}")
#
# subtask1_deadline = timezone.now() + timedelta(days=2)
# subtask1 = SubTask.objects.create(
#     title="Gather information",
#     description="Find necessary information for the presentation",
#     status="New",
#     deadline=subtask1_deadline,
#     task=task_new
# )
# print(f"Создана подзадача: {subtask1.title}")
#
# subtask2_deadline = timezone.now() + timedelta(days=1)
# subtask2 = SubTask.objects.create(
#     title="Create slides",
#     description="Create presentation slides",
#     status="New",
#     deadline=subtask2_deadline,
#     task=task_new
# )
# print(f"Создана подзадача: {subtask2.title}")

# task_new = Task.objects.filter(status="new")
#
# print("\nЗадачи со статусом 'New': \n")
#
# for task in task_new:
#     print(f"{task.title:<27} ({task.status:<3}) --- {task.deadline}")
# print("_"*65)
#
# subtask_done = SubTask.objects.filter(
#     status="done",
#     deadline__lt=timezone.now()
# )
#
# if subtask_done.exists():
#     print("\nПросроченные подзадачи со статусом 'Done':\n")
#
#     for subtask in subtask_done:
#         print(f"{subtask.title:<27} ({subtask.status:<3}) --- {subtask.deadline}")
#
# else:
#     print("\nПросроченныx подзадач со статусом 'Done' не найдено.")

# Обновление задачи "Prepare presentation"
# try:
#     task = Task.objects.get(title="Prepare presentation")
#     task.status = "in_progress"
#     task.save()
#     print(f"Обновлена задача: {task.title} - статус изменен на 'In Progress'")
# except Task.DoesNotExist:
#     print("Задача 'Prepare presentation' не найдена")
#
# # Обновление подзадачи "Gather information"
# try:
#     subtask1 = SubTask.objects.get(title="Gather information")
#     subtask1.deadline = timezone.now() - timedelta(days=2)
#     subtask1.save()
#     print(f"Обновлена подзадача: {subtask1.title} - дедлайн изменен на {subtask1.deadline}")
# except SubTask.DoesNotExist:
#     print("Подзадача 'Gather information' не найдена")
#
# # Обновление подзадачи "Create slides"
# try:
#     subtask2 = SubTask.objects.get(title="Create slides")
#     subtask2.description = "Create and format presentation slides"
#     subtask2.save()
#     print(f"Обновлена подзадача: {subtask2.title} - описание изменено")
# except SubTask.DoesNotExist:
#     print("Подзадача 'Create slides' не найдена")


# В модели SubTask установлен on_delete=models.CASCADE,
# следовательно, подзадачи удалятся автоматически при удалении задачи
# try:
#     task = Task.objects.get(title="Prepare presentation")
#     task_title = task.title
#     task.delete()
#     print(f"Удалена задача: '{task_title}' и все связанные подзадачи")
#
# except Task.DoesNotExist:
#     print("Задача 'Prepare presentation' не найдена")
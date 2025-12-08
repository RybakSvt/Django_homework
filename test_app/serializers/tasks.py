from django.utils import timezone
from rest_framework import serializers

from test_app.models import Task
from test_app.serializers.subtasks import SubTaskSerializer
from test_app.serializers.categories import CategorySerializer



class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Task
        fields = [
            'title',
            'description',
            'status',
            'deadline',
            'categories',
        ]

    def validate_deadline(self, value: str) -> str:
        if value < timezone.now():
            raise serializers.ValidationError(
                "Срок выполнения задачи должен быть позже текущей даты"
            )
        return value


class TaskListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    # Владелец виден при чтении
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'deadline',
            'categories',
            'owner_username'
        ]

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


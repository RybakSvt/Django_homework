from rest_framework import serializers

from test_app.models import SubTask


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = [
            'title',
            'description',
            'status',
            'deadline',
            'created_at',
        ]


class SubTaskSerializer(serializers.ModelSerializer):

    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = SubTask
        fields = [
            'id',
            'title',
            'description',
            'status',
            'deadline',
            'owner_username',
            'task',
        ]
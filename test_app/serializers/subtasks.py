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
    class Meta:
        model = SubTask
        fields = [
            'title',
            'description',
            'status',
            'deadline',
        ]
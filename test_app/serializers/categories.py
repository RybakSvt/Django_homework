from rest_framework import serializers

from test_app.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data['name']

        category, created = Category.objects.get_or_create(
            name=name,
            defaults=validated_data
        )

        if not created:
            raise serializers.ValidationError({
                "name": f"Категория '{name}' уже существует"

            })

        return category

    def update(self, instance, validated_data):
        name = validated_data['name']

        if name != instance.name:
            if Category.objects.filter(name=name).exclude(pk=instance.pk).exists():
                raise serializers.ValidationError({
                    "name": f"Категория '{name}' уже существует"

                })

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from test_app.models import Category
from test_app.serializers import CategorySerializer, CategoryCreateSerializer


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        return CategoryCreateSerializer if self.request.method == 'POST' else CategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            category = serializer.save()
        except Exception as exc:
            return Response(
                data={
                    "error": "Ошибка сохранения категории",
                    "detail": str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            data=CategorySerializer(category).data,
            status=status.HTTP_201_CREATED
        )


class CategoryDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        return CategoryCreateSerializer if self.request.method in ['PUT', 'PATCH'] else CategorySerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            self.perform_update(serializer)
        except Exception as exc:
            return Response(
                data={"error": f"Ошибка при обновлении категории: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            self.perform_destroy(instance)
        except Exception as exc:
            return Response(
                data={"error": f"Ошибка при удалении категории: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(data={}, status=status.HTTP_204_NO_CONTENT)
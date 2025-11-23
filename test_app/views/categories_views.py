from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, serializers

from test_app.models import Category
from test_app.serializers import (
    CategorySerializer,
    CategoryCreateSerializer,
)


class CategoryListCreateView(APIView):

    def get(self, request: Request) -> Response:
        categories = Category.objects.all()
        categories_dto = CategorySerializer(categories, many=True)
        return Response(
            data=categories_dto.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        category_dto = CategoryCreateSerializer(data=request.data)
        if not category_dto.is_valid():
            return Response(
                data=category_dto.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            category = category_dto.save()
        except serializers.ValidationError as exc:
            return Response(
                data=exc.detail,
                status=status.HTTP_400_BAD_REQUEST
            )
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


class CategoryDetailUpdateDeleteView(APIView):

    def get_object(self, category_id: int):
        try:
            return Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return None

    def _handle_save_error(self, exc):
        """Обработка ошибок при сохранении категории"""
        if isinstance(exc, serializers.ValidationError):
            return Response(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                data={"error": f"Ошибка при сохранении категории: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request: Request, category_id: int) -> Response:
        category = self.get_object(category_id)
        if not category:
            return Response(
                data={"error": f"Категория с id={category_id} не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        category_dto = CategorySerializer(category)
        return Response(
            data=category_dto.data,
            status=status.HTTP_200_OK
        )

    def put(self, request: Request, category_id: int) -> Response:
        category = self.get_object(category_id)
        if not category:
            return Response(
                data={"error": f"Категория с id={category_id} не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        category_dto = CategoryCreateSerializer(instance=category, data=request.data)
        if not category_dto.is_valid():
            return Response(
                data=category_dto.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            category_dto.save()
        except Exception as exc:
            return self._handle_save_error(exc)

        return Response(
            data=category_dto.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request: Request, category_id: int) -> Response:
        category = self.get_object(category_id)
        if not category:
            return Response(
                data={"error": f"Категория с id={category_id} не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        category_dto = CategoryCreateSerializer(instance=category, data=request.data, partial=True)
        if not category_dto.is_valid():
            return Response(
                data=category_dto.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            category_dto.save()
        except Exception as exc:
            return self._handle_save_error(exc)

        return Response(
            data=category_dto.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request: Request, category_id: int) -> Response:
        category = self.get_object(category_id)
        if not category:
            return Response(
                data={"error": f"Категория с id={category_id} не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            category.delete()
        except Exception as exc:
            return Response(
                data={"error": f"Ошибка при удалении категории: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            data={},
            status=status.HTTP_204_NO_CONTENT
        )


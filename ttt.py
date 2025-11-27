class BookListCreateAPIView(APIView):

    def get_filtered_queryset(self, query_params):
        # queryset = model.objects.all()  # SELECT * FROM books;
        queryset = Book.objects.all()  # SELECT * FROM books;

        author_last_name = query_params.get('last_name')
        author_first_name = query_params.get('first_name')

        if author_last_name:
            queryset = queryset.filter(
                author__last_name=author_last_name
            )  # SELECT * FROM books WHERE author_last_name = 'author_last_name';

        if author_first_name:
            queryset = queryset.filter(
                author__first_name=author_first_name
            )

        return queryset

    def get(self, request: Request) -> Response:
        books = self.get_filtered_queryset(request.query_params)
        books_dto = BookListSerializer(books, many=True)

        return Response(
            data=books_dto.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        # DTO
        # D  - ata
        # T  - ransfer
        # O  - bject
        book_dto = BookCreateSerializer(data=request.data)

        if not book_dto.is_valid():
            return Response(
                data=book_dto.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            book_dto.save()
        except Exception as exc:
            return Response(
                data={"error": f"Ошибка при сохранении книги: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            data=book_dto.data,
            status=status.HTTP_201_CREATED
        )

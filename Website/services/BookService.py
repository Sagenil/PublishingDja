from ..repositories.BookRepository import BookRepository
from ..serializers import BookSerializer


class BookService:
    def __init__(self):
        self.book_repository = BookRepository()

    def add_book(self, request_data):
        book = BookSerializer(data=request_data)
        if not book.is_valid():
            raise ValueError("Book: One or more fields didn't pass validation")
        return self.book_repository.add(**book.validated_data)

    def update_book(self, id, request_data):
        if request_data.get('created_at') is not None:
            raise ValueError("You can't change created_at attribute")
        if request_data.get('product_id') is not None:
            raise ValueError("You can't change product_id attribute")
        book = self.get_book_by_id(id)
        book_data = BookSerializer(instance=book, data=request_data, partial=True)
        if book_data.is_valid():
            return self.book_repository.update(id, **book_data.validated_data)

    def get_all_books(self):
        return self.book_repository.get_all()

    def get_book_by_id(self, id):
        book = self.book_repository.get_by_id(id)
        if len(book) == 0:
            raise ValueError(f"No book with id {id} was found")
        return book.first()

    def delete_book(self, id):
        if not self.book_repository.get_by_id(id).exists():
            raise ValueError(f"No book with id {id} was found")
        return self.book_repository.delete(id)

    @staticmethod
    def serialize(books, many=False):
        serializer = BookSerializer(books, many=many)
        return serializer

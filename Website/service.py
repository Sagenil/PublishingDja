import datetime

from django.core.handlers.wsgi import WSGIRequest

from .services.BookService import BookService
from .services.ProductService import ProductService
from .services.StickerService import StickerService

product_service = ProductService()
book_service = BookService()
sticker_service = StickerService()


def add_product(request):
    request_data = request.data
    product = product_service.add_product(request_data)
    request_data['product_id'] = product.id
    if product.type == product.ProductType.BOOK:
        try:
            book = book_service.add_book(request_data)
            return product, book
        except Exception as e:
            print(e)
            product_service.delete_product(product.id)
            return None
    elif product.type == product.ProductType.STICKER:
        try:
            sticker = sticker_service.add_sticker(request_data)
            return product, sticker
        except Exception as e:
            print(e)
            product_service.delete_product(product.id)
            return None


def get_product(id):
    return product_service.get_product_by_id(id)


def get_product_by_name(name):
    return product_service.get_product_by_name(name)


def get_combined_product(id):
    product = product_service.get_product_by_id(id)
    if product.type == product.ProductType.BOOK:
        book = book_service.get_book_by_id(product.id)
        return product, book
    elif product.type == product.ProductType.STICKER:
        sticker = sticker_service.get_sticker_by_id(product.id)
        return product, sticker


def get_all_products():
    return product_service.get_all_products()


def get_book(id):
    return book_service.get_book_by_id(id)


def get_all_books():
    return book_service.get_all_books()


def get_sticker(id):
    return sticker_service.get_sticker_by_id(id)


def get_all_stickers():
    return sticker_service.get_all_stickers()
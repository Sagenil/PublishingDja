from django.db import models

from ..models import *


class AggregatedRepository:
    @staticmethod
    def get_books_grouped_by_price():
        books = (Book.objects.select_related('product_id')
            .values("product_id__price", "product_id__name")
            .order_by("product_id__price"))
        return books

    @staticmethod
    def get_stickers_grouped_by_price():
        stickers = (Sticker.objects.select_related('product_id')
                    .values("product_id__price", "product_id__name")
                    .order_by("product_id__price"))
        return stickers

    @staticmethod
    def count_books_by_genre():
        books = (Book.objects.values("genre")
                 .annotate(count=models.Count("genre"))
                 .order_by("genre"))
        return books

    @staticmethod
    def get_average_books_price():
        price = (Book.objects
                 .select_related("product_id")
                 .aggregate(average_price=models.Avg("product_id__price")))
        return price

    @staticmethod
    def get_books_price_distribution():
        distribution = (Book.objects
                        .select_related("product_id")
                        .annotate(price_range=models.Case(
                            models.When(product_id__price__lt=199.99, then=models.Value("<199,99 UAH")),
                            models.When(product_id_price__gte=199.99, then=models.Value("199,99-299,99 UAH")),
                            models.When(product_id__price__gte=299.99, then=models.Value("299,99-399,99 UAH")),
                            models.When(product_id__price__gte=399.99, then=models.Value("399,99-499,99 UAH")),
                            models.When(product_id__price__gte=499.99, then=models.Value(">499,99 UAH")),
                            output_field=models.FloatField
                        ))
                        .values("price_range")
                        .annotate(count=models.Count("id"))
                        .order_by("price_range"))
        return distribution

    @staticmethod
    def get_stickers_price_distribution():
        distribution = (Sticker.objects
                        .select_related("product_id")
                        .annotate(price_range=models.Case(
                        models.When(product_id__price__lt=199.99, then=models.Value("<199,99 UAH")),
                            models.When(product_id_price__gte=199.99, then=models.Value("199,99-299,99 UAH")),
                            models.When(product_id__price__gte=299.99, then=models.Value("299,99-399,99 UAH")),
                            models.When(product_id__price__gte=399.99, then=models.Value("399,99-499,99 UAH")),
                            models.When(product_id__price__gte=499.99, then=models.Value(">499,99 UAH")),
                            output_field=models.FloatField
                        ))
                        .values("price_range")
                        .annotate(count=models.Count("id"))
                        .order_by("price_range"))
        return distribution

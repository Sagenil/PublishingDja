import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    bonuses = models.FloatField(default=0)
    # groups = models.ManyToManyField(
    #     Group,
    #     related_name="customuser_groups",  # Custom related_name to avoid clashes
    #     blank=True,
    #     help_text='The groups this user belongs to.',
    #     verbose_name='groups',
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name="customuser_permissions",  # Custom related_name to avoid clashes
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     verbose_name='user permissions',
    # )


# Create your models here.
class Product(models.Model):
    class ProductType(models.TextChoices):
        BOOK = "BOOK"
        STICKER = "STICKER"
    type = models.CharField(max_length=64, choices=ProductType.choices, default=ProductType.BOOK)
    name = models.CharField(max_length=64, unique=True)
    title_image = models.CharField(max_length=128, unique=True, null=True)
    price = models.FloatField(default=0)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now())


class Book(models.Model):
    author = models.CharField(max_length=64)
    genre = models.CharField(max_length=64)
    product_id = models.OneToOneField(Product, models.CASCADE)


class Sticker(models.Model):
    material = models.CharField(max_length=64)
    product_id = models.OneToOneField(Product, models.CASCADE)

"""
URL configuration for PublishingDja project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from Website import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name="index"),
    path('product/new/book', views.add_book_view, name="add_book"),
    path('product/new/sticker', views.add_sticker_view, name="add_sticker"),
    path('api/product', views.get_product_by_name),
    path('api/product/<int:id>', views.get_product, name="product"),
    path('api/product/all', views.get_all_products),
    path('api/product/new', views.add_product),
    path('api/product/update/<int:id>', views.update_product),
    path('api/product/delete/<int:id>', views.delete_product),
    path('api/book/<int:id>', views.get_book),
    path('api/book/all', views.get_all_books),
    path('api/book/update/<int:id>', views.update_book),
    path('api/sticker/<int:id>', views.get_sticker),
    path('api/sticker/all', views.get_all_stickers),
    path('api/sticker/update/<int:id>', views.update_sticker),
    path('api/token/', views.CustomTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/register/', views.RegisterView.as_view()),
    path('api/profile/', views.get_profile),
    path('api/profile/update/', views.update_profile),
    path('foreignapi/account/new/', views.add_bank_account),
    path('foreignapi/account', views.get_bank_account_by_email),
    path('foreignapi/account/all/', views.get_all_bank_accounts, name='bank_accounts'),
    path('foreignapi/account/delete/<int:id>', views.delete_bank_account),
    path('foreignapi/account/delete/view', views.delete_bank_account_view, name="delete_bank_account"),
]

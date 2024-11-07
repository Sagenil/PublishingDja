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
    path('api/product', views.get_product_by_params),
    path('api/product/<int:id>', views.get_product),
    path('api/product/new', views.add_product),
    path('api/product/update/<int:id>', views.update_product),
    path('api/product/delete/<int:id>', views.delete_product),
    path('api/book/<int:id>', views.get_book),
    path('api/book/new', views.add_book),
    path('api/book/update/<int:id>', views.update_book),
    path('api/book/delete/<int:id>', views.delete_book),
    path('api/sticker/<int:id>', views.get_sticker),
    path('api/sticker/new', views.add_sticker),
    path('api/sticker/update/<int:id>', views.update_sticker),
    path('api/sticker/delete/<int:id>', views.delete_sticker),
    path('api/token/', views.CustomTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/register/', views.RegisterView.as_view()),
    path('api/profile/', views.get_profile),
    path('api/profile/update/', views.update_profile),
]

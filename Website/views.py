from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView

from . import service
from .repositories.CustomUserRepository import CustomUserRepository
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer


custom_user_repository = CustomUserRepository()


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = custom_user_repository.get_all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    serializer = ProfileSerializer(user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = ProfileSerializer(user, data=request.data, partial=True)
    if not serializer.is_valid():
        CustomUserRepository.add(**serializer.data)
    return Response(serializer.data)


@api_view(['GET'])
def get_product_by_name(request):
    name = request.GET.get("name")
    if name is None:
        raise ValueError("Required parameter name not specified")
    product = service.get_product_by_name(name)
    product_data = service.serialize_product(product).data
    return Response(product_data)


@api_view(['GET'])
def get_product(request, id):
    product = service.get_product(id)
    product_data = service.serialize_product(product).data
    return Response(product_data)


@api_view(['GET'])
def get_all_products(request):
    products = service.get_all_products()
    products_data = service.serialize_products(products).data
    return Response(products_data)


@api_view(['POST'])
def add_product(request):
    try:
        service.add_product(request)
        return Response(status=201)
    except Exception as e:
        return Response(status=500, data={"error": e})


@api_view(['PUT'])
def update_product(request, id):
    service.update_product(id, request)
    return Response()


@api_view(['DELETE'])
def delete_product(request, id):
    service.delete_product(id)
    return Response()


@api_view(['GET'])
def get_book(request, id):
    book = service.get_book(id)
    book_data = service.serialize_book(book).data
    return Response(book_data)


@api_view(['GET'])
def get_all_books(request):
    books = service.get_all_books()
    books_data = service.serialize_books(books).data
    return Response(books_data)


@api_view(['PUT'])
def update_book(request, id):
    service.update_book(id, request)
    return Response()


@api_view(['GET'])
def get_sticker(request, id):
    sticker = service.get_sticker(id)
    sticker_data = service.serialize_sticker(sticker).data
    return Response(sticker_data)


@api_view(['GET'])
def get_all_stickers(request):
    stickers = service.get_all_stickers()
    stickers_data = service.serialize_stickers(stickers).data
    return Response(stickers_data)


@api_view(['PUT'])
def update_sticker(request, id):
    service.update_sticker(id, request)
    return Response()

from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView

from .services.BookService import BookService
from .services.ProductService import ProductService
from .services.StickerService import StickerService
from . import service
from .repositories.CustomUserRepository import CustomUserRepository
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer


product_service = ProductService()
book_service = BookService()
sticker_service = StickerService()
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
def get_product_by_params(request):
    name = request.GET.get("name")
    if name is None:
        raise ValueError("Required parameter name not specified")
    product = product_service.get_product_by_name(name)
    product_data = product_service.serialize(product).data
    return Response(product_data)


@api_view(['GET'])
def get_product(request, id):
    product = product_service.get_product_by_id(id)
    product_data = product_service.serialize(product).data
    return Response(product_data)


@api_view(['POST'])
def add_product(request):
    service.add_product(request)
    return Response()


@api_view(['PUT'])
def update_product(request, id):
    product_service.update_product(id, request.data)
    return Response()


@api_view(['DELETE'])
def delete_product(request, id):
    product_service.delete_product(id)
    return Response()


@api_view(['GET'])
def get_book(request, id):
    book = book_service.get_book_by_id(id)
    book_data = book_service.serialize(book).data
    return Response(book_data)


@api_view(['POST'])
def add_book(request):
    book_service.add_book(request.data)
    return Response()


@api_view(['PUT'])
def update_book(request, id):
    book_service.update_book(id, request.data)
    return Response()


@api_view(['DELETE'])
def delete_book(request, id):
    book_service.delete_book(id)
    return Response()


@api_view(['GET'])
def get_sticker(request, id):
    sticker = sticker_service.get_sticker_by_id(id)
    sticker_data = sticker_service.serialize(sticker).data
    return Response(sticker_data)


@api_view(['POST'])
def add_sticker(request):
    sticker_service.add_sticker(request.data)
    return Response()


@api_view(['PUT'])
def update_sticker(request, id):
    sticker_service.update_sticker(id, request.data)
    return Response()


@api_view(['DELETE'])
def delete_sticker(request, id):
    sticker_service.delete_sticker(id)
    return Response()



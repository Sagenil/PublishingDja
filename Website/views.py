from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView

import plotly.express as px
from bokeh.plotting import figure
from bokeh.embed import components
import pandas as pd
from math import pi
from bokeh.transform import cumsum
from bokeh.palettes import Category20c
from bokeh.models import ColumnDataSource

from . import service, NetworkHelper
from .repositories.AggregatedRepository import AggregatedRepository
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


# Actual pages
@api_view(['GET'])
def index(request):
    products = service.get_all_products()
    template = loader.get_template("Website/index.html")
    context = {
        "products_list": products
    }
    return HttpResponse(template.render(context, request))


def add_book_view(request):
    if request.method == 'POST':
        service.add_product(request)
        return redirect('index')
    return render(request, "Website/addBook.html")


def add_sticker_view(request):
    if request.method == 'POST':
        service.add_product(request)
        return redirect('index')
    return render(request, "Website/addSticker.html")


@api_view(['POST'])
def add_bank_account(request):
    response = NetworkHelper.add_account(request)
    return Response(status=response.status_code)


@api_view(['GET'])
def get_bank_account_by_email(request):
    email = request.GET.get("email")
    response = NetworkHelper.get_account_by_email(email)
    return Response(response.json(), status=response.status_code)


@api_view(['GET'])
def get_all_bank_accounts(request):
    response = NetworkHelper.get_all_accounts()
    return Response(response.json(), status=response.status_code)


@api_view(['DELETE'])
def delete_bank_account(request, id):
    response = NetworkHelper.delete_account(id)
    return Response(status=response.status_code)


def delete_bank_account_view(request):
    if request.method == 'POST':
        NetworkHelper.delete_account(request.POST.get('id'))
        return redirect('bank_accounts')
    accounts_list = NetworkHelper.get_all_accounts().json()
    return render(request, "Website/bankAccounts.html", {'accounts_list': accounts_list})


def books_graphs_view(request):
    top_n = int(request.GET.get("top", 20))
    graph_type = request.GET.get("graph_type", "bar")

    books_by_price = list(AggregatedRepository.get_books_grouped_by_price())
    df_books_by_price = pd.DataFrame(books_by_price)

    print(df_books_by_price["product_id__name"])
    print(df_books_by_price["product_id__price"])
    df_books_by_price = df_books_by_price.sort_values("product_id__price", ascending=False).head(top_n)

    if graph_type == "bar":
        plotly_fig = px.bar(
            df_books_by_price,
            x="product_id__price",
            y="product_id__name",
            title=f"Top {top_n} Books Grouped by Price (Bar Graph)",
            labels={"product_id__price": "Price", "product_id__name": "Book Name"}
        )
    elif graph_type == "scatter":
        plotly_fig = px.scatter(
            df_books_by_price,
            x="product_id__price",
            y="product_id__name",
            title=f"Top {top_n} Books Grouped by Price (Scatter Plot)",
            labels={"product_id__price": "Price", "product_id__name": "Book Name"}
        )
    elif graph_type == "pie":
        plotly_fig = px.pie(
            df_books_by_price,
            names="product_id__name",
            values="product_id__price",
            title=f"Top {top_n} Books Grouped by Price (Pie Chart)"
        )
    else:
        plotly_fig = px.bar(
            df_books_by_price,
            x="product_id__price",
            y="product_id__name",
            title=f"Top {top_n} Books Grouped by Price (Default Bar Graph)",
            labels={"product_id__price": "Price", "product_id__name": "Book Name"}
        )
    plotly_chart = plotly_fig.to_html(full_html=False)

    bokeh_fig = figure(
        title=f"Top {top_n} Books Grouped by Price (Bokeh Bar Graph)",
        x_range=df_books_by_price["product_id__name"].tolist(),
        tools="pan,wheel_zoom,box_zoom,reset,save",
        toolbar_location="above",
        width=800,
        height=400
    )
    bokeh_fig.vbar(
        x=df_books_by_price["product_id__name"].tolist(),
        top=df_books_by_price["product_id__price"].tolist(),
        width=0.8,
        color="navy"
    )
    bokeh_script, bokeh_div = components(bokeh_fig)
    print("Bokeh Script:", bokeh_script)
    print("Bokeh Div:", bokeh_div)

    context = {
        "plotly_chart": plotly_chart,
        "bokeh_script": bokeh_script,
        "bokeh_div": bokeh_div,
        "top_n": top_n,
        "graph_type": graph_type,
    }
    return render(request, "Website/bookGraphs.html", context)


def distribution_graphs_view(request):
    top_n = int(request.GET.get("top", 20))
    graph_type = request.GET.get("graph_type", "pie")
    product_type = request.GET.get("product_type", "books")

    if product_type == "books":
        price_distribution = AggregatedRepository.get_books_price_distribution()
    else:
        price_distribution = AggregatedRepository.get_stickers_price_distribution()

    df_price_distribution = pd.DataFrame(price_distribution)
    df_price_distribution = df_price_distribution.sort_values("count", ascending=False).head(top_n)

    if graph_type == "bar":
        plotly_fig = px.bar(
            df_price_distribution,
            x="count",
            y="price_range",
            orientation="h",
            title=f"Top {top_n} {product_type.capitalize()} by Price Range (Bar Graph)",
            labels={"count": "Count", "price_range": "Price Range"}
        )
    elif graph_type == "scatter":
        plotly_fig = px.scatter(
            df_price_distribution,
            x="price_range",
            y="count",
            title=f"Top {top_n} {product_type.capitalize()} by Price Range (Scatter Plot)",
            labels={"price_range": "Price Range", "count": "Count"}
        )
    else:
        plotly_fig = px.pie(
            df_price_distribution,
            names="price_range",
            values="count",
            title=f"Top {top_n} {product_type.capitalize()} by Price Range (Pie Chart)"
        )
    plotly_chart = plotly_fig.to_html(full_html=False)

    available_sizes = sorted(Category20c.keys())  # Valid keys in Category20c
    num_colors = min(len(df_price_distribution), available_sizes[-1])
    closest_size = next((size for size in available_sizes if size >= num_colors), available_sizes[-1])
    palette = Category20c[closest_size]
    df_price_distribution['angle'] = df_price_distribution['count'] / df_price_distribution['count'].sum() * 2 * pi
    df_price_distribution['color'] = [palette[i % num_colors] for i in range(len(df_price_distribution))]

    bokeh_fig = figure(
        title=f"Top {top_n} {product_type.capitalize()} by Price Range (Bokeh Pie Chart)",
        toolbar_location=None,
        tools="hover",
        tooltips="@price_range: @count",
        width=800,
        height=400
    )

    bokeh_fig.wedge(
        x=0, y=0, radius=0.4,
        start_angle=cumsum('angle', include_zero=True),
        end_angle=cumsum('angle'),
        line_color="white",
        fill_color='color',
        legend_field='price_range',
        source=ColumnDataSource(df_price_distribution)
    )

    bokeh_fig.axis.axis_label = None
    bokeh_fig.axis.visible = False
    bokeh_fig.grid.grid_line_color = None

    bokeh_script, bokeh_div = components(bokeh_fig)

    context = {
        "plotly_chart": plotly_chart,
        "bokeh_script": bokeh_script,
        "bokeh_div": bokeh_div,
        "top_n": top_n,
        "graph_type": graph_type,
        "item_type": product_type,
    }
    return render(request, "Website/priceDistributionGraphs.html", context)

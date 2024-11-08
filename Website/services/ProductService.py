import datetime

from ..repositories.ProductRepository import ProductRepository
from ..serializers import ProductSerializer


class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()

    def add_product(self, request_data: dict):
        request_data['created_at'] = datetime.datetime.now()
        product = ProductSerializer(data=request_data)
        if not product.is_valid():
            raise ValueError("Product: One or more fields didn't pass validation")
        name = product.data['name']
        if self.product_repository.get_by_name(name).exists():
            raise ValueError(f"There already is product with {name} name")
        return self.product_repository.add(**product.validated_data)

    def get_all_products(self):
        return self.product_repository.get_all()

    def get_product_by_id(self, id):
        product = self.product_repository.get_by_id(id)
        if len(product) == 0:
            raise ValueError(f"No product with id {id} was found")
        return product.first()

    def get_product_by_name(self, name):
        product = self.product_repository.get_by_name(name)
        if len(product) == 0:
            raise ValueError(f"No product with name {name} was found")
        return product.first()

    def update_product(self, id, request_data: dict):
        if request_data.get('created_at') is not None:
            raise ValueError("You can't change created_at attribute")
        name = request_data.get('name')
        if self.product_repository.get_by_name(name).exists():
            raise ValueError(f"There already is product with name {name}")
        product = self.get_product_by_id(id)
        product_data = ProductSerializer(instance=product, data=request_data, partial=True)
        if product_data.is_valid():
            return self.product_repository.update(id, **product_data.validated_data)

    def delete_product(self, id):
        if not self.product_repository.get_by_id(id).exists():
            raise ValueError(f"No product with id {id} was found")
        return self.product_repository.delete(id)

    @staticmethod
    def serialize(products, many=False):
        serializer = ProductSerializer(products, many=many)
        return serializer

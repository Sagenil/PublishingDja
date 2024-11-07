from ..models import Sticker


class StickerRepository:
    def __init__(self):
        self.model = Sticker

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, product_id):
        return self.model.objects.filter(id=product_id)

    def add(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update(self, product_id, **kwargs):
        return self.model.objects.filter(id=product_id).update(**kwargs)

    def delete(self, product_id):
        return self.model.objects.filter(id=product_id).delete()
from ..repositories.StickerRepository import StickerRepository
from ..serializers import StickerSerializer


class StickerService:
    def __init__(self):
        self.sticker_repository = StickerRepository()

    def add_sticker(self, request_data):
        sticker = StickerSerializer(data=request_data)
        if not sticker.is_valid():
            raise ValueError("Sticker: One or more fields didn't pass validation")
        return self.sticker_repository.add(**sticker.validated_data)

    def update_sticker(self, id, request_data):
        if request_data.get('created_at') is not None:
            raise ValueError("You can't change created_at attribute")
        if request_data.get('product_id') is not None:
            raise ValueError("You can't change product_id attribute")
        sticker = self.get_sticker_by_id(id)
        sticker_data = StickerSerializer(instance=sticker, data=request_data, partial=True)
        if sticker_data.is_valid():
            return self.sticker_repository.update(id, **sticker_data.validated_data)

    def get_all_stickers(self):
        return self.sticker_repository.get_all()

    def get_sticker_by_id(self, id):
        sticker = self.sticker_repository.get_by_id(id)
        if len(sticker) == 0:
            raise ValueError(f"No sticker with id {id} was found")
        return sticker.first()

    def delete_sticker(self, id):
        if not self.sticker_repository.get_by_id(id).exists():
            raise ValueError(f"No sticker with id {id} was found")
        return self.sticker_repository.delete(id)

    @staticmethod
    def serialize(stickers, many=False):
        serializer = StickerSerializer(stickers, many=many)
        return serializer

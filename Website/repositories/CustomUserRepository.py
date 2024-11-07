from ..models import CustomUser


class CustomUserRepository:
    def __init__(self):
        self.model = CustomUser

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, product_id):
        return self.model.objects.filter(id=product_id)

    def get_by_username(self, username):
        return self.model.objects.filter(name=username)

    def get_by_email(self, email):
        return self.model.objects.filter(email=email)

    def add(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update(self, product_id, **kwargs):
        return self.model.objects.filter(id=product_id).update(**kwargs)

    def delete(self, product_id):
        return self.model.objects.filter(id=product_id).delete()
from graphene_django.types import DjangoObjectType
import graphene
from apps.product.models import Product, Category


class ProductType(DjangoObjectType):
    id = graphene.ID(required=True)
    class Meta:
        model = Product
        fields = "__all__"
    def resolve_id(self, info):
        return self.id

class CategoryType(DjangoObjectType):
    id = graphene.ID(required=True)
    class Meta:
        model = Category
        fields = "__all__"
    def resolve_id(self, info):
        return self.id
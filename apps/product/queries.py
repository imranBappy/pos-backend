import graphene

from .models import Category, Product
from apps.base.utils import get_object_by_kwargs
from .objectType import CategoryType, ProductType


class Query(graphene.ObjectType):
    category = graphene.Field(CategoryType, id=graphene.ID(required=True))
    categories = graphene.List(CategoryType)
    Product = graphene.Field(ProductType, id=graphene.ID(required=True))
    products = graphene.List(ProductType)

    def resolve_category(self, info, id):
        return get_object_by_kwargs(Category, {"id": id})
     
    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_product(self, info, id):
        return get_object_by_kwargs(Product, {"id": id})
     
    def resolve_products(self, info):
        return Product.objects.all()
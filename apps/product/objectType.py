from graphene_django.types import DjangoObjectType
import graphene
from .models import Ingredient, TableBooking, Product, Category, Order, OrderProduct,Floor, FloorTable, ExtraFood, Payment
from .filters import IngredientFilter, TableBookingFilter, ProductFilter, CategoryFilter, OrderFilter, OrderProductFilter ,FloorFilter, FloorTableFilter,  PaymentFilter
from backend.count_connection import CountConnection
from apps.accounts.objectType import UserType

class TableBookingType(DjangoObjectType):
    id = graphene.ID(required=True)
    class Meta:
        model = TableBooking
        filterset_class = TableBookingFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class IngredientType(DjangoObjectType):
    id = graphene.ID(required=True)
    price = graphene.Float()
    class Meta:
        model = Ingredient
        filterset_class = IngredientFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class ProductType(DjangoObjectType):
    id = graphene.ID(required=True)
    price = graphene.Float()
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection
        

class CategoryType(DjangoObjectType):
    id = graphene.ID(required=True)
    is_category = graphene.Boolean()
    class Meta:
        model = Category
        filterset_class = CategoryFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class SubCategoryType(CategoryType):
    parent_id = graphene.ID(required=True)
    class Meta:
        model = Category
        filterset_class = CategoryFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class OrderType(DjangoObjectType):
    id = graphene.ID(required=True)
    user = graphene.Field(UserType)
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class OrderProductType(DjangoObjectType):
    id = graphene.ID(required=True)
    class Meta:
        model = OrderProduct
        filterset_class = OrderProductFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection




class FloorType(DjangoObjectType):
    id = graphene.ID(required=True)
    class Meta:
        model = Floor
        filterset_class = FloorFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection
    
class FloorTableType(DjangoObjectType):
    id = graphene.ID(required=True)
    class Meta:
        model = FloorTable
        filterset_class = FloorTableFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class PaymentType(DjangoObjectType):
    id = graphene.ID(required=True)
    
    class Meta:
        model = Payment
        filterset_class = PaymentFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection        





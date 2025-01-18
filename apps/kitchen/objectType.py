import graphene
from .models import Kitchen, KitchenOrder, Printer
from graphene_django import DjangoObjectType
from .filters import KitchenFilter, KitchenOrderFilter, PrinterFilter
from backend.count_connection import CountConnection


class KitchenType(DjangoObjectType):
    id = graphene.ID(required=True)
    class Meta:
        model = Kitchen
        fields = "__all__"
        filterset_class = KitchenFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class KitchenOrderType(DjangoObjectType):
    class Meta:
        model = KitchenOrder
        fields = "__all__"
        filterset_class = KitchenOrderFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class PrinterType(DjangoObjectType):
    class Meta:
        model = Printer
        fields = "__all__"
        filterset_class = PrinterFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection
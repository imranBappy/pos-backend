import graphene
from backend.count_connection import CountConnection
from graphene_django import DjangoObjectType
from .models import Unit, Supplier, SupplierInvoice, SupplierPayment, ItemCategory, Item, ParchageInvoiceItem, Waste, WasteItem
from .filters import UnitFilter, SupplierFilter, SupplierInvoiceFilter, SupplierPaymentFilter, ItemCategoryFilter, ItemFilter, ParchageInvoiceItemFilter, WasteFilter, WasteItemFilter


class UnitType(DjangoObjectType):
    id = graphene.ID(required=True)
    
    class Meta:
        model = Unit
        filterset_class = UnitFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class SupplierType(DjangoObjectType):
    id = graphene.ID(required=True)
    
    class Meta:
        model = Supplier
        filterset_class = SupplierFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class SupplierInvoiceType(DjangoObjectType):
    id = graphene.ID(required=True)
    
    class Meta:
        model = SupplierInvoice
        filterset_class = SupplierInvoiceFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class SupplierPaymentType(DjangoObjectType):
    id = graphene.ID(required=True)
    
    class Meta:
        model = SupplierPayment
        filterset_class = SupplierPaymentFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class ItemCategoryType(DjangoObjectType):
    id = graphene.ID(required=True)
    
    class Meta:
        model = ItemCategory
        filterset_class = ItemCategoryFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class ItemType(DjangoObjectType):
    id = graphene.ID(required=True)
    
    class Meta:
        model = Item
        filterset_class = ItemFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class ParchageInvoiceItemType(DjangoObjectType):
    id = graphene.ID(required=True)
    
    class Meta:
        model = ParchageInvoiceItem
        filterset_class = ParchageInvoiceItemFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class WasteType(DjangoObjectType):
    id = graphene.ID(required=True)
    
    class Meta:
        model = Waste
        filterset_class = WasteFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class WasteItemType(DjangoObjectType):
    id = graphene.ID(required=True)
    
    class Meta:
        model = WasteItem
        filterset_class = WasteItemFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

import graphene
from backend.count_connection import CountConnection
from graphene_django import DjangoObjectType
from apps.inventory.models import Unit,WasteCategory, Supplier, SupplierInvoice, SupplierPayment, ItemCategory, Item, ParchageInvoiceItem, Waste, WasteItem
from apps.inventory.filters import WasteCategoryFilter, UnitFilter, SupplierFilter, SupplierInvoiceFilter, SupplierPaymentFilter, ItemCategoryFilter, ItemFilter, ParchageInvoiceItemFilter, WasteFilter, WasteItemFilter


class WasteCategoryType(DjangoObjectType):
    id = graphene.ID(required=True)
    class Meta:
        model = WasteCategory
        filterset_class = WasteCategoryFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

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
    stock_level = graphene.Float(required=True)  # Add stock_level as a field
    
    class Meta:
        model = Item
        filterset_class = ItemFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

        
    def resolve_stock_level(self, info):
        if self.safety_stock == 0:
            return float('inf') if self.current_stock > 0 else 0
        return self.current_stock / self.safety_stock

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

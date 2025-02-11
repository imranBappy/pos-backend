import graphene
from graphene_django.filter import DjangoFilterConnectionField
from .models import Unit, Supplier, SupplierInvoice, SupplierPayment, ItemCategory, Item, ParchageInvoiceItem, Waste, WasteItem
from .inputObjectTypes import UnitType, SupplierType, SupplierInvoiceType, SupplierPaymentType, ItemCategoryType, ItemType, ParchageInvoiceItemType, WasteType, WasteItemType
from apps.base.utils import get_object_by_kwargs
from backend.authentication import isAuthenticated
from apps.accounts.models import UserRole

class Query(graphene.ObjectType):
    unit = graphene.Field(UnitType, id=graphene.ID(required=True))
    units = DjangoFilterConnectionField(UnitType)

    supplier = graphene.Field(SupplierType, id=graphene.ID(required=True))
    suppliers = DjangoFilterConnectionField(SupplierType)

    supplier_invoice = graphene.Field(SupplierInvoiceType, id=graphene.ID(required=True))
    supplier_invoices = DjangoFilterConnectionField(SupplierInvoiceType)

    supplier_payment = graphene.Field(SupplierPaymentType, id=graphene.ID(required=True))
    supplier_payments = DjangoFilterConnectionField(SupplierPaymentType)

    item_category = graphene.Field(ItemCategoryType, id=graphene.ID(required=True))
    item_categories = DjangoFilterConnectionField(ItemCategoryType)

    item = graphene.Field(ItemType, id=graphene.ID(required=True))
    items = DjangoFilterConnectionField(ItemType)

    parchage_invoice_item = graphene.Field(ParchageInvoiceItemType, id=graphene.ID(required=True))
    parchage_invoice_items = DjangoFilterConnectionField(ParchageInvoiceItemType)

    waste = graphene.Field(WasteType, id=graphene.ID(required=True))
    wastes = DjangoFilterConnectionField(WasteType)
    
    waste_item = graphene.Field(WasteItemType, id=graphene.ID(required=True))
    waste_items = DjangoFilterConnectionField(WasteItemType)

    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER, UserRole.CHEF, UserRole.WAITER])
    def resolve_unit(self, info, id):
        return get_object_by_kwargs(Unit, {"id": id})

    @isAuthenticated([UserRole.ADMIN])
    def resolve_units(self, info, **kwargs):
        return Unit.objects.all()

    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER, UserRole.CHEF, UserRole.WAITER])
    def resolve_supplier(self, info, id):
        return get_object_by_kwargs(Supplier, {"id": id})

    @isAuthenticated([UserRole.ADMIN])
    def resolve_suppliers(self, info, **kwargs):
        return Supplier.objects.all()

    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER, UserRole.CHEF, UserRole.WAITER])
    def resolve_supplier_invoice(self, info, id):
        return get_object_by_kwargs(SupplierInvoice, {"id": id})

    @isAuthenticated([UserRole.ADMIN])
    def resolve_supplier_invoices(self, info, **kwargs):
        return SupplierInvoice.objects.all()

    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER, UserRole.CHEF, UserRole.WAITER])
    def resolve_supplier_payment(self, info, id):
        return get_object_by_kwargs(SupplierPayment, {"id": id})

    @isAuthenticated([UserRole.ADMIN])
    def resolve_supplier_payments(self, info, **kwargs):
        return SupplierPayment.objects.all()

    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER, UserRole.CHEF, UserRole.WAITER])
    def resolve_item_category(self, info, id):
        return get_object_by_kwargs(ItemCategory, {"id": id})

    @isAuthenticated([UserRole.ADMIN])
    def resolve_item_categories(self, info, **kwargs):
        return ItemCategory.objects.all()

    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER, UserRole.CHEF, UserRole.WAITER])
    def resolve_item(self, info, id):
        return get_object_by_kwargs(Item, {"id": id})

    # @isAuthenticated([UserRole.ADMIN])
    def resolve_items(self, info, **kwargs):
        return Item.objects.all()

    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER, UserRole.CHEF, UserRole.WAITER])
    def resolve_parchage_invoice_item(self, info, id):
        return get_object_by_kwargs(ParchageInvoiceItem, {"id": id})

    @isAuthenticated([UserRole.ADMIN])
    def resolve_parchage_invoice_items(self, info, **kwargs):
        return ParchageInvoiceItem.objects.all()

    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER, UserRole.CHEF, UserRole.WAITER])
    def resolve_waste(self, info, id):
        return get_object_by_kwargs(Waste, {"id": id})

    @isAuthenticated([UserRole.ADMIN])
    def resolve_wastes(self, info, **kwargs):
        return Waste.objects.all()

    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER, UserRole.CHEF, UserRole.WAITER])
    def resolve_waste_item(self, info, id):
        return get_object_by_kwargs(WasteItem, {"id": id})

    @isAuthenticated([UserRole.ADMIN])
    def resolve_waste_items(self, info, **kwargs):
        return WasteItem.objects.all()

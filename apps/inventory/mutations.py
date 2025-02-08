import graphene
from graphene_django.forms.mutation import DjangoFormMutation
from .models import Unit, Supplier, SupplierInvoice, SupplierPayment, ItemCategory, Item, ParchageInvoiceItem, Waste, WasteItem
from .forms import UnitForm, SupplierForm, SupplierInvoiceForm, SupplierPaymentForm, ItemCategoryForm, ItemForm, ParchageInvoiceItemForm, WasteForm, WasteItemForm
from .inputObjectTypes import UnitType, SupplierType, SupplierInvoiceType, SupplierPaymentType, ItemCategoryType, ItemType, ParchageInvoiceItemType, WasteType, WasteItemType
from apps.base.utils import get_object_or_none, create_graphql_error
from backend.authentication import isAuthenticated
from apps.accounts.models import UserRole

class UnitCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    unit = graphene.Field(UnitType)

    class Meta:
        form_class = UnitForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(Unit, id=input.get('id'))
        form = UnitForm(input, instance=instance)
        if form.is_valid():
            unit = form.save()
            return UnitCUD(
                message="Unit processed successfully",
                success=True,
                unit=unit
            )
        create_graphql_error(form)

class SupplierCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    supplier = graphene.Field(SupplierType)

    class Meta:
        form_class = SupplierForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(Supplier, id=input.get('id'))
        form = SupplierForm(input, instance=instance)
        if form.is_valid():
            supplier = form.save()
            return SupplierCUD(
                message="Supplier processed successfully",
                success=True,
                supplier=supplier
            )
        create_graphql_error(form)
class SupplierInvoiceCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    supplier_invoice = graphene.Field(SupplierInvoiceType)

    class Meta:
        form_class = SupplierInvoiceForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(SupplierInvoice, id=input.get('id'))
        form = SupplierInvoiceForm(input, instance=instance)
        if form.is_valid():
            supplier_invoice = form.save()
            return SupplierInvoiceCUD(
                message="Supplier Invoice processed successfully",
                success=True,
                supplier_invoice=supplier_invoice
            )
        create_graphql_error(form)

class SupplierPaymentCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    supplier_payment = graphene.Field(SupplierPaymentType)

    class Meta:
        form_class = SupplierPaymentForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(SupplierPayment, id=input.get('id'))
        form = SupplierPaymentForm(input, instance=instance)
        if form.is_valid():
            supplier_payment = form.save()
            return SupplierPaymentCUD(
                message="Supplier Payment processed successfully",
                success=True,
                supplier_payment=supplier_payment
            )
        create_graphql_error(form)

class ItemCategoryCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    item_category = graphene.Field(ItemCategoryType)

    class Meta:
        form_class = ItemCategoryForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(ItemCategory, id=input.get('id'))
        form = ItemCategoryForm(input, instance=instance)
        if form.is_valid():
            item_category = form.save()
            return ItemCategoryCUD(
                message="Item Category processed successfully",
                success=True,
                item_category=item_category
            )
        create_graphql_error(form)

class ItemCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    item = graphene.Field(ItemType)

    class Meta:
        form_class = ItemForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(Item, id=input.get('id'))
        form = ItemForm(input, instance=instance)
        if form.is_valid():
            item = form.save()
            return ItemCUD(
                message="Item processed successfully",
                success=True,
                item=item
            )
        create_graphql_error(form)

class ParchageInvoiceItemCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    parchage_invoice_item = graphene.Field(ParchageInvoiceItemType)

    class Meta:
        form_class = ParchageInvoiceItemForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(ParchageInvoiceItem, id=input.get('id'))
        form = ParchageInvoiceItemForm(input, instance=instance)
        if form.is_valid():
            parchage_invoice_item = form.save()
            return ParchageInvoiceItemCUD(
                message="Purchase Invoice Item processed successfully",
                success=True,
                parchage_invoice_item=parchage_invoice_item
            )
        create_graphql_error(form)

class WasteCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    waste = graphene.Field(WasteType)

    class Meta:
        form_class = WasteForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(Waste, id=input.get('id'))
        form = WasteForm(input, instance=instance)
        if form.is_valid():
            waste = form.save()
            return WasteCUD(
                message="Waste record processed successfully",
                success=True,
                waste=waste
            )
        create_graphql_error(form)

class WasteItemCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    waste_item = graphene.Field(WasteItemType)

    class Meta:
        form_class = WasteItemForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(WasteItem, id=input.get('id'))
        form = WasteItemForm(input, instance=instance)
        if form.is_valid():
            waste_item = form.save()
            return WasteItemCUD(
                message="Waste Item processed successfully",
                success=True,
                waste_item=waste_item
            )
        create_graphql_error(form)

class DeleteUnit(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()  

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate(self, info, id):
        try:
            unit = Unit.objects.get(pk=id)
            unit.delete()
            return DeleteUnit(success=True)  # Return success=True
        except Unit.DoesNotExist:
            return DeleteUnit(success=False)  # Return success=False

class DeleteSupplier(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()  

    def mutate(self, info, id):
        try:
            supplier = Supplier.objects.get(pk=id)
            supplier.delete()
            return DeleteSupplier(success=True)  # Return success=True
        except Supplier.DoesNotExist:
            return DeleteSupplier(success=False)  # Return success=False


class DeleteSupplierInvoice(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            supplierInvoice = SupplierInvoice.objects.get(pk=id)
            supplierInvoice.delete()
            return DeleteSupplierInvoice(success=True)
        except SupplierInvoice.DoesNotExist:
            return DeleteSupplierInvoice(success=False)

class DeleteSupplierPayment(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            supplierPayment = SupplierPayment.objects.get(pk=id)
            supplierPayment.delete()
            return DeleteSupplierPayment(success=True)
        except SupplierPayment.DoesNotExist:
            return DeleteSupplierPayment(success=False)

class DeleteItemCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            itemCategory = ItemCategory.objects.get(pk=id)
            itemCategory.delete()
            return DeleteItemCategory(success=True)
        except ItemCategory.DoesNotExist:
            return DeleteItemCategory(success=False)

class DeleteItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            item = Item.objects.get(pk=id)
            item.delete()
            return DeleteItem(success=True)
        except Item.DoesNotExist:
            return DeleteItem(success=False)

class DeleteParchageInvoiceItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            parchageInvoiceItem = ParchageInvoiceItem.objects.get(pk=id)
            parchageInvoiceItem.delete()
            return DeleteParchageInvoiceItem(success=True)
        except ParchageInvoiceItem.DoesNotExist:
            return DeleteParchageInvoiceItem(success=False)

class DeleteWaste(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            waste = Waste.objects.get(pk=id)
            waste.delete()
            return DeleteWaste(success=True)
        except Waste.DoesNotExist:
            return DeleteWaste(success=False)

class DeleteWasteItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            wasteItem = WasteItem.objects.get(pk=id)
            wasteItem.delete()
            return DeleteWasteItem(success=True)
        except WasteItem.DoesNotExist:
            return DeleteWasteItem(success=False)
        
        
class Mutation(graphene.ObjectType):
    unit_cud = UnitCUD.Field()
    supplier_cud = SupplierCUD.Field()
    supplier_invoice_cud = SupplierInvoiceCUD.Field()
    supplier_payment_cud = SupplierPaymentCUD.Field()
    item_category_cud = ItemCategoryCUD.Field()
    item_cud = ItemCUD.Field()
    parchage_invoice_item_cud = ParchageInvoiceItemCUD.Field()
    waste_cud = WasteCUD.Field()
    waste_item_cud = WasteItemCUD.Field()

    # Delete Mutations
    delete_unit = DeleteUnit.Field()
    delete_supplier = DeleteSupplier.Field()
    delete_supplier_invoice = DeleteSupplierInvoice.Field()
    delete_supplier_payment = DeleteSupplierPayment.Field()
    delete_item_category = DeleteItemCategory.Field()
    delete_item = DeleteItem.Field()
    delete_parchage_invoice_item = DeleteParchageInvoiceItem.Field()
    delete_waste = DeleteWaste.Field()
    delete_waste_item = DeleteWasteItem.Field()
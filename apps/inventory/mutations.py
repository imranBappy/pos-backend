from decimal import Decimal
import graphene
from graphene_django.forms.mutation import DjangoFormMutation
from apps.inventory.models import (
    InvoiceConsumption,
    WasteCategory,
    Unit,
    Supplier,
    SupplierInvoice,
    SupplierPayment,
    ItemCategory,
    Item,
    PurchaseInvoiceItem,
    Waste,
    WasteItem,
)
from apps.inventory.forms import (
    WasteCategoryForm,
    UnitForm,
    SupplierForm,
    SupplierInvoiceForm,
    SupplierPaymentForm,
    ItemCategoryForm,
    ItemForm,
    PurchaseInvoiceItemForm,
    WasteForm,
    WasteItemForm,
)
from apps.inventory.objectTypes import (
    UnitType,
    SupplierType,
    SupplierInvoiceType,
    SupplierPaymentType,
    ItemCategoryType,
    ItemType,
    PurchaseInvoiceItemType,
    WasteType,
    WasteItemType,
)
from apps.base.utils import get_object_or_none, create_graphql_error
from backend.authentication import isAuthenticated
from apps.accounts.models import User, UserRole
from apps.product.models import ORDER_STATUS_CHOICES
from apps.product.models import PAYMENT_STATUS_CHOICES
from graphql import GraphQLError
from django.db import transaction


class WasteCategoryCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()

    class Meta:
        form_class = WasteCategoryForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(WasteCategory, id=input.get("id"))
        form = WasteCategoryForm(input, instance=instance)
        if form.is_valid():
            form.save()
            return WasteCategoryCUD(
                message="Category created successfully",
                success=True,
            )
        create_graphql_error(form)


class UnitCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    unit = graphene.Field(UnitType)

    class Meta:
        form_class = UnitForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(Unit, id=input.get("id"))
        form = UnitForm(input, instance=instance)
        if form.is_valid():
            unit = form.save()
            return UnitCUD(
                message="Unit processed successfully", success=True, unit=unit
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
        instance = get_object_or_none(Supplier, id=input.get("id"))
        form = SupplierForm(input, instance=instance)
        if form.is_valid():
            supplier = form.save()
            return SupplierCUD(
                message="Supplier processed successfully",
                success=True,
                supplier=supplier,
            )
        print(form)
        create_graphql_error(form)


# class PurchaseInvoiceItemType(graphene.InputObjectType):
#     item = graphene.ID(required=True)
#     quantity = graphene.Decimal(required=True)
#     price = graphene.Decimal(required=True)

# class SupplierInvoiceInputType(graphene.InputObjectType):
#     due_payment_date = graphene.Date(required=False)
#     invoice_number = graphene.String(required=True)
#     po_number =  graphene.String(required=True)
#     supplier = graphene.ID(required=False)
#     invoice_image = graphene.String(required=False)
#     items = graphene.List(PurchaseInvoiceItemType, required=True)


# class SupplierInvoiceCUV2(graphene.Mutation):
#     class Arguments:
#         input = SupplierInvoiceInputType(required=True)

#     # success = graphene.
#     pass


class SupplierInvoiceCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    supplier_invoice = graphene.Field(SupplierInvoiceType)

    class Meta:
        form_class = SupplierInvoiceForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(SupplierInvoice, id=input.get("id"))
        form = SupplierInvoiceForm(input, instance=instance)

        if form.is_valid():
            supplier_invoice = form.save()
            return SupplierInvoiceCUD(
                message="Supplier Invoice processed successfully",
                success=True,
                supplier_invoice=supplier_invoice,
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
        try:
            instance = get_object_or_none(SupplierPayment, id=input.get("id"))
            form = SupplierPaymentForm(input, instance=instance)
            invoice = SupplierInvoice.objects.get(id=input.get("invoice"))

            if invoice.amount < input.get("amount"):
                raise GraphQLError(
                    message="Payment amount is greater than order amount!"
                )
            #  minimum payment amount is 1
            if input.get("amount") < 1:
                raise GraphQLError(message="Payment amount should be greater than 1!")

            if not form.is_valid():
                create_graphql_error(form)

            # if order is already completed, then return error
            if invoice.status == ORDER_STATUS_CHOICES.COMPLETED:
                raise GraphQLError(message="Purchase is already completed!")

            # calculate total paid amount
            total_paid_amount = 0
            if invoice.payments:
                for payment in invoice.payments.all():
                    if payment.status == PAYMENT_STATUS_CHOICES.COMPLETED:
                        total_paid_amount += payment.amount

            # check if payment amount is greater than order amount
            if total_paid_amount + input.get("amount") > invoice.amount:
                raise GraphQLError(
                    message="Payment amount is greater than order amount!"
                )

            # save payment
            newPayment = form.save()

            total_paid_amount += input.get("amount")

            # update order status
            if total_paid_amount >= invoice.amount:
                invoice.status = ORDER_STATUS_CHOICES.COMPLETED
                invoice.due = 0  # fully paid

            # update order status and due
            if total_paid_amount < invoice.amount:
                invoice.status = ORDER_STATUS_CHOICES.DUE
                invoice.due = invoice.amount - total_paid_amount

            invoice.due_payment_date = input.get("due_payment_date")

            invoice.paid_amount = total_paid_amount
            invoice.save()
            newPayment = SupplierPayment.objects.get(id=newPayment.id)

            return SupplierPaymentCUD(
                message="Supplier Payment processed successfully",
                success=True,
                supplier_payment=newPayment,
            )
        except Exception as e:
            print(e)
            return GraphQLError(message="Payment failed!")


class ItemCategoryCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    item_category = graphene.Field(ItemCategoryType)

    class Meta:
        form_class = ItemCategoryForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(ItemCategory, id=input.get("id"))
        form = ItemCategoryForm(input, instance=instance)
        if form.is_valid():
            item_category = form.save()
            return ItemCategoryCUD(
                message="Item Category processed successfully",
                success=True,
                item_category=item_category,
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
        try:
            instance = get_object_or_none(Item, id=input.get("id"))
            form = ItemForm(input, instance=instance)
            if form.is_valid():
                item = form.save()
                return ItemCUD(
                    message="Item processed successfully", success=True, item=item
                )
            print(form.errors)
            create_graphql_error(form)
        except Exception as e:
            print(e)


class PurchaseInvoiceItemCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    purchase_invoice_item = graphene.Field(PurchaseInvoiceItemType)

    class Meta:
        form_class = PurchaseInvoiceItemForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(PurchaseInvoiceItem, id=input.get("id"))

        if not input.get("total_quantity"):
            input["total_quantity"] = input.get("quantity")

        form = PurchaseInvoiceItemForm(input, instance=instance)

        item = Item.objects.get(id=input.get("item"))
        if not input.get("id"):  # item stock update for  create operation
            item.stock = item.stock + input.get("quantity")
            item.current_stock = item.current_stock + input.get("quantity")

        if input.get("id"):  #  item stock update for update operation
            pre_quantity = instance.quantity
            current_quantity = input.get("quantity")
            item.stock = (item.stock - pre_quantity) + current_quantity
            item.current_stock = (item.current_stock - pre_quantity) + current_quantity

        # item save
        item.save()

        if form.is_valid():
            purchase_invoice_item = form.save()

            return PurchaseInvoiceItemCUD(
                message="Purchase Invoice Item processed successfully",
                success=True,
                purchase_invoice_item=purchase_invoice_item,
            )
        create_graphql_error(form)


class WasteItemInputType(graphene.InputObjectType):
    ingredient = graphene.String(required=True)
    quantity = graphene.Decimal(required=True)


class CreateWasteInputType(graphene.InputObjectType):
    date = graphene.Date(required=True)
    category = graphene.String(required=True)
    responsible = graphene.String(required=False)
    notes = graphene.String(required=False)
    items = graphene.List(WasteItemInputType, required=True)
    invoice = graphene.String(required=False)


class CreateWaste(graphene.Mutation):
    class Arguments:
        input = CreateWasteInputType(required=True)

    success = graphene.Boolean()

    def mutate(root, info, input):
        try:
            with transaction.atomic():
                # Step 1: Retrieve required objects
                invoice = CreateWaste.get_supplier_invoice(input["items"][0])

                # Step 2: Validate that all waste items come from the same invoice
                if invoice:
                    CreateWaste.validate_invoice_items(invoice, input.items)

                # Step 3: Create Waste record
                waste_data = {
                    "date": input.date,
                    "category": CreateWaste.get_waste_category(input.category),
                    "responsible": CreateWaste.get_responsible_user(input.responsible)
                    if input.responsible
                    else None,
                    "invoice": invoice,
                    "notes": input.notes,
                    "estimated_cost": Decimal(0),
                }

                waste = Waste.objects.create(**waste_data)

                # Step 4: Process Waste Items and Calculate Estimated Cost
                estimated_cost = CreateWaste.process_waste_items(
                    waste, input.items, invoice
                )

                # Step 5: Update estimated_cost
                waste.estimated_cost = estimated_cost
                waste.save()
                
                return CreateWaste(success=True)
        except Exception as e:
            print(e)
            raise GraphQLError(str(e))

    @staticmethod
    def get_waste_category(categoryId):
        """Retrieve WasteCategory or raise an error if not found"""
        try:
            return WasteCategory.objects.get(id=categoryId)
        except WasteCategory.DoesNotExist:
            raise ValueError(f"Invalid waste category: {categoryId}")

    @staticmethod
    def get_supplier_invoice(item):
        """Retrieve SupplierInvoice or raise an error if not found"""
        try:
            purchase_invoice_item = (
                PurchaseInvoiceItem.objects.filter(
                    item=item["ingredient"], quantity__gt=0
                )
                .order_by("created_at")
                .first()
            )
            return purchase_invoice_item.supplier_Invoice
        except SupplierInvoice.DoesNotExist:
            raise ValueError("Invoice  not found")

    @staticmethod
    def get_responsible_user(userId):
        """Retrieve User or raise an error if not found"""
        try:
            return User.objects.get(id=userId)
        except User.DoesNotExist:
            raise ValueError(f"User {userId} not found")

    @staticmethod
    def validate_invoice_items(invoice, items):
        """Ensure all waste items belong to the given invoice"""
        invoice_item_ids = set(
            PurchaseInvoiceItem.objects.filter(supplier_Invoice=invoice).values_list(
                "item__id", flat=True
            )
        )

        for item_data in items:
            item = Item.objects.get(id=item_data.ingredient)
            if item.id not in invoice_item_ids:
                raise ValueError(
                    f"Item {item.name} does not belong to invoice {invoice.invoice_number}"
                )

    @staticmethod
    def process_waste_items(waste, items, invoice):
        """Handles stock validation, stock deduction, updates PurchaseInvoiceItem, and calculates estimated cost"""
        total_loss_amount = Decimal(0)

        for item_data in items:
            item = Item.objects.get(id=item_data.ingredient)
            purchase_item = PurchaseInvoiceItem.objects.filter(
                item=item, supplier_Invoice=invoice.id
            ).first()

            # Validate stock availability
            if item.current_stock < item_data.quantity:
                raise ValueError(
                    f"Not enough stock for {item.name}. Available: {item.current_stock}, Needed: {item_data.quantity}"
                )

            # Deduct stock from Item
            item.current_stock -= item_data.quantity
            item.stock -= item_data.quantity
            item.save()

            # Determine item price for loss_amount calculation
            price_per_unit = 0

            if purchase_item:
                price_per_unit = purchase_item.price  # Use invoice price

            loss_amount = price_per_unit * Decimal(item_data.quantity)
            total_loss_amount += loss_amount

            # Deduct from ParchageInvoiceItem if invoice is linked
            if invoice and purchase_item:
                if purchase_item.quantity < item_data.quantity:
                    raise ValueError(
                        f"Cannot waste {item_data.quantity} of {item.name}, only {purchase_item.quantity} available in invoice."
                    )

                purchase_item.quantity -= item_data.quantity
                purchase_item.save()

            # Create WasteItem entry
            waste_item = WasteItem.objects.create(
                waste=waste,
                ingredient=item,
                quantity=item_data.quantity,
                loss_amount=loss_amount,
            )

            InvoiceConsumption.objects.create(
                waste_item=waste_item,
                purchase_invoice_item=purchase_item,
                quantity=item_data.quantity,
            )


        return total_loss_amount


class WasteCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    waste = graphene.Field(WasteType)

    class Meta:
        form_class = WasteForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(Waste, id=input.get("id"))
        form = WasteForm(input, instance=instance)
        if form.is_valid():
            waste = form.save()
            return WasteCUD(
                message="Waste record processed successfully", success=True, waste=waste
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
        instance = get_object_or_none(WasteItem, id=input.get("id"))
        form = WasteItemForm(input, instance=instance)
        if form.is_valid():
            waste_item = form.save()
            return WasteItemCUD(
                message="Waste Item processed successfully",
                success=True,
                waste_item=waste_item,
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
        except Exception as e:
            raise GraphQLError(e)
            


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


class DeletePurchaseInvoiceItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            purchaseInvoiceItem = PurchaseInvoiceItem.objects.get(pk=id)

            # item stock update
            item = Item.objects.get(id=purchaseInvoiceItem.item.id)
            pre_quantity = purchaseInvoiceItem.quantity
            item.stock = item.stock - pre_quantity
            item.current_stock = item.current_stock - pre_quantity
            item.save()

            purchaseInvoiceItem.delete()
            return DeletePurchaseInvoiceItem(success=True)
        except PurchaseInvoiceItem.DoesNotExist:
            return DeletePurchaseInvoiceItem(success=False)


class DeleteWaste(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            with transaction.atomic():
                print("hitted")
                waste = Waste.objects.get(pk=id)
                waste_ingredient = WasteItem.objects.filter(waste=waste)
                
                for item in waste_ingredient:
                    item.ingredient.current_stock = Decimal(item.ingredient.current_stock) + Decimal(item.quantity)
                    item.ingredient.save()
                    invoice_consumption = InvoiceConsumption.objects.get(waste_item=item)
                    invoice_consumption.purchase_invoice_item.quantity = Decimal(invoice_consumption.purchase_invoice_item.quantity) + Decimal(invoice_consumption.quantity)
                    invoice_consumption.purchase_invoice_item.save()

                waste.delete()
                return DeleteWaste(success=True)
        except Exception as e:
            print(e)
            raise GraphQLError(e)


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
    purchase_invoice_item_cud = PurchaseInvoiceItemCUD.Field()
    waste_cud = WasteCUD.Field()
    waste_item_cud = WasteItemCUD.Field()
    create_waste = CreateWaste.Field()
    waste_category_cud = WasteCategoryCUD.Field()

    # Delete Mutations
    delete_unit = DeleteUnit.Field()
    delete_supplier = DeleteSupplier.Field()
    delete_supplier_invoice = DeleteSupplierInvoice.Field()
    delete_supplier_payment = DeleteSupplierPayment.Field()
    delete_item_category = DeleteItemCategory.Field()
    delete_item = DeleteItem.Field()
    delete_purchase_invoice_item = DeletePurchaseInvoiceItem.Field()
    delete_waste = DeleteWaste.Field()

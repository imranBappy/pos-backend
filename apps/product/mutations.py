from decimal import Decimal
import graphene
from apps.base.utils import get_object_or_none, create_graphql_error
from apps.inventory.models import InvoiceConsumption, PurchaseInvoiceItem
from .objectType import IngredientType , CategoryType, ProductType, OrderType, PaymentType
from apps.base.utils import get_object_by_kwargs
from backend.authentication import isAuthenticated
from django.db import transaction
from graphene_django.forms.mutation import DjangoFormMutation
from .forms import IngredientForm, ProductForm, CategoryForm, OrderForm, OrderProductForm, FloorForm, FloorTableForm, PaymentForm
from apps.product.models import Ingredient, Category, OrderIngredients,TableBooking, Product, Order,ORDER_STATUS_CHOICES,PAYMENT_STATUS_CHOICES, OrderProduct, Floor, FloorTable, Payment
from apps.accounts.models import  UserRole
import json 
from django.utils.timezone import now
from datetime import timedelta
from apps.product.tasks import release_expired_bookings, booking_expired
from graphql import GraphQLError
import random
import string



class IngredientCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    ingredient = graphene.Field(IngredientType)
    
    class Meta:
        form_class = IngredientForm
    
    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
            
        instance = get_object_or_none(Ingredient, id=input.get('id'))
        form = IngredientForm(input, instance=instance)
        if not form.is_valid(): 
            create_graphql_error(form)
        
        ingredient = form.save()
        return IngredientCUD(
                message="Created successfully",
                success=True,
                ingredient=ingredient
            )

class CategoryCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    category = graphene.Field(CategoryType)
    
    class Meta:
        form_class = CategoryForm
    
    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
            
        instance = get_object_or_none(Category, id=input.get('id'))
        form = CategoryForm(input, instance=instance)
        if form.is_valid():
            category = form.save()
            return CategoryCUD(
                message="Created successfully",
                success=True,
                category=category
            )
        create_graphql_error(form)
        
class ProductCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    product = graphene.Field(ProductType)

    class Meta:
        form_class = ProductForm

    @isAuthenticated([UserRole.MANAGER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        
        instance = get_object_or_none(Product, id=input.get("id"))
        form = ProductForm(input, instance=instance)
        
        
        if form.is_valid():
            product = form.save()
            return ProductCUD(
                message="Created successfully!", 
                success=True,
                product=product
            )
        
        # response proper error message
        create_graphql_error(form.errors) 
        

class DeleteProduct(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()    
    class Arguments:
        id = graphene.ID(required=True)
    
    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER])
    def mutate(self, info, id):
        product = get_object_by_kwargs(Product, {"id": id})
        product.delete()
        return DeleteProduct(success=True, message="Deleted!")


class OrderProductInputType(graphene.InputObjectType):
    product = graphene.ID(required=True)
    quantity = graphene.Int(required=True)
    discount = graphene.Decimal(required=True)

class OrderInputType(graphene.InputObjectType):
    user = graphene.ID(required=False) # update able
    type = graphene.String(required=True) # update able
    due_payment_date =  graphene.String(required=False) # update able
    status = graphene.String(required=True) # update able
    outlet = graphene.String(required=True)
    order_id = graphene.String(required=True)
    is_cart = graphene.Boolean(required=False) # update able
    table_bookings = graphene.String(required=False)

    items = graphene.List(OrderProductInputType, required=True)

class OrderCU(graphene.Mutation):
    class Arguments:
        input = OrderInputType(required=True)
    
    message = graphene.String()
    success = graphene.Boolean()
    order = graphene.Field(OrderType)

    def mutate(root, info, input):
        try:
            with transaction.atomic():
                items =  input.get('items')
                final_amount = 0
                amount = 0
                
                # form validation
                orderInput = {
                        "user" : input['user'],
                        "type" : input['type'],
                        "due_payment_date"  : input['due_payment_date'],
                        "status" : input['status'],
                        "outlet" : input['outlet'],
                        "order_id": input['order_id'],
                        "is_cart" : input['is_cart'],
                }
                orderForm = OrderForm(orderInput)
                if not orderForm.is_valid():
                    raise create_graphql_error(orderForm)
                
                order = get_object_or_none(Order, order_id=input.get('order_id'))

                if not order.status == ORDER_STATUS_CHOICES.PENDING :
                    raise GraphQLError(message="This order is not updateable")
                
                if not order:
                    order = Order.objects.create(**orderInput)

                
                    
                # validation: ingredient are avaible, minmum quantity
                for item in items:
                    ingredients =  Ingredient.objects.filter(product=item['product'])
                    quantity  = item['quantity']
                    for ingredient in ingredients:
                        
                        total_quantity = quantity * ingredient.quantity
                        current_stock = ingredient.item.current_stock
                        if (current_stock - total_quantity ) < 0:
                            raise GraphQLError(success=False,message=f"There is no enough {ingredient.item.name} in stock.")
                    
                
                        # update item stock
                        ingredient.item.current_stock = current_stock -  total_quantity
                        ingredient.item.save()

                    instance = get_object_or_none(OrderProduct, id=item['id'])
                    orderProductForm = OrderProductForm(item, instance=instance)
                    if not orderProductForm.is_valid():
                        raise create_graphql_error(orderProductForm)
                    orderProductForm.save()

                    product = Product.objects.get(id=item['product'])

                    amount+= (product * quantity)
                    vat  = (amount // 100) * product.vat
                    final_amount+= (product * quantity) + (vat * quantity)


                # calculate total paid amount
                total_paid_amount = 0
                if order.payments :
                    for payment in order.payments.all():
                        if payment.status == PAYMENT_STATUS_CHOICES.COMPLETED:
                            total_paid_amount += payment.amount

                order.due = final_amount
                order.status = ORDER_STATUS_CHOICES.PENDING

                # update order status
                if total_paid_amount >= order.final_amount:
                    order.status = ORDER_STATUS_CHOICES.COMPLETED
                    order.due = 0 # fully paid

                # update order status and due
                if total_paid_amount < order.final_amount and total_paid_amount > 0:
                    order.status = ORDER_STATUS_CHOICES.DUE
                    order.due = order.final_amount - total_paid_amount
                    order.is_cart = False

                order.save()


                OrderCU(message="Success", success=True, order=order)
        except Exception as e:
            raise GraphQLError(message=e)
            

    def _get_or_create_order(input):
        """Retrieve existing order or create a new one."""
        pass

    def _validate_order_status(order):
        """Ensure the order is in a modifiable state."""
        pass

    def _validate_stock_and_update(items):
        """Check ingredient stock levels and update inventory accordingly."""
        pass

    def _calculate_final_amount(items):
        """Calculate total order amount including VAT."""
        pass


class OrderCUV2(graphene.Mutation):
    class Arguments:
        input = OrderInputType(required=True)
    
    message = graphene.String()
    success = graphene.Boolean()
    order = graphene.Field(OrderType)

    @isAuthenticated(
            [
                UserRole.ADMIN, UserRole.MANAGER
            ]
    )
    def mutate(root, info, input):
        try:
            with transaction.atomic():
               
                OrderCUV2._validate_order_status(input.get('order_id'))
                
                items = input.get('items',[])
                final_amount, amount = OrderCUV2._calculate_amounts(items)

                input['amount'] = f'{amount}'
                input['final_amount'] = f'{final_amount}'
                input['due'] = f'{final_amount}'
                
                order, is_new = OrderCUV2._get_or_create_order(input)
                
                if not is_new:
                    OrderCUV2._restore_stock_and_delete_items(order)
                
                OrderCUV2._validate_stock_and_update(items, order.id)
                OrderCUV2._book_table(table_bookings=input.get('table_bookings'),order=order)

                return OrderCUV2(message="Success", success=True, order=order)
        except Exception as e:
            print(e)
            raise GraphQLError(message=e)
            

    def _get_or_create_order(input):
        """Retrieve existing order or create a new one."""
        is_new = False
        order = get_object_or_none(Order, order_id=input.get('order_id'))
        
        if not order:
            is_new = True

        orderForm = OrderForm(input, instance=order)
        print(orderForm.errors)
        if not orderForm.is_valid():
            raise create_graphql_error(orderForm)
        
        order = orderForm.save()

        return order, is_new

    def _validate_order_status( order_id):
        """Ensure the order is in a modifiable state."""
        order = get_object_or_none(Order, order_id=order_id)
        if order and order.status != ORDER_STATUS_CHOICES.PENDING:
            raise GraphQLError("This order is not updateable")
        

    def _validate_stock_and_update(items, orderId):
        """Check ingredient stock levels and update inventory accordingly."""
        for item in items:
            product = Product.objects.get(id=item['product'])
            quantity = item['quantity']

            if not product:
                raise GraphQLError("Product does not exist.")

            product_price = Decimal(product.price)
            discount =  Decimal(item.discount)
            if (product_price - discount) < 0 :
                return GraphQLError("Can't discount more than 100%")
            item_amount = (product_price - discount) * quantity

            item['vat'] = product.vat
            item['price'] = item_amount
            item['order'] = orderId
            if not orderId:
                raise GraphQLError("Order has not created.")
            
            if not item.discount:
                item['discount'] = 0

            orderProductForm = OrderProductForm(item)
            if not orderProductForm.is_valid():
                print(orderProductForm.errors)
                raise create_graphql_error(orderProductForm)
            orderProduct = orderProductForm.save()

            ingredients = Ingredient.objects.filter(product=product)
            for ingredient in ingredients:
                required_stock = quantity * Decimal(ingredient.quantity)
                if ingredient.item.current_stock < required_stock:
                    raise GraphQLError(f"Not enough {ingredient.item.name} in stock.")

                ingredient.item.current_stock -= required_stock
                ingredient.item.save()
                
                # new update 
                order_ingredient = OrderIngredients.objects.create(
                    quantity=required_stock,
                    order_product = orderProduct,
                    item = ingredient.item,
                )
                
                order_ingredients_consumption = order_ingredient
                needed_items = []
                purchase_invoice_item = PurchaseInvoiceItem.objects.filter(item=ingredient.item.id, quantity__gt=0).order_by('created_at')

                temp  = 0
                for needed_item in purchase_invoice_item:
                    if temp > required_stock:
                        break
                    
                    needed_items.append(needed_item)
                    temp +=needed_item.quantity

                if  temp < required_stock:
                    raise GraphQLError(f"Not enough {ingredient.item.name} in stock.")
           
                temp2  = required_stock
                for needed_item in needed_items:
                    if 0 == temp2 :
                        break
                    
                    if needed_item.quantity <=  temp2 :
                        InvoiceConsumption.objects.create(
                            order_ingredients_consumption=order_ingredients_consumption,
                            purchase_invoice_item=needed_item,
                            quantity=needed_item.quantity,
                        )
                        temp2 = temp2 - needed_item.quantity
                        needed_item.quantity = 0
                        needed_item.save()
                        
                    elif needed_item.quantity > temp2 and temp2 > 0:
                        if (needed_item.quantity - temp2) < 0:
                            raise GraphQLError("There is no enough in stock.")
                        
                        InvoiceConsumption.objects.create(
                            order_ingredients_consumption=order_ingredients_consumption,
                            purchase_invoice_item=needed_item,
                            quantity=temp2,
                        )
                        needed_item.quantity  = needed_item.quantity - temp2
                        needed_item.save()
                        temp2 = 0

                

    def _calculate_amounts(items):
        """Calculate total order amount including VAT."""
        total_amount = Decimal(0)
        amount = Decimal(0)

        for item in items:
            product = Product.objects.get(id=item['product'])
            quantity = item['quantity']
            
            product_price = Decimal(product.price)
            discount =  Decimal(item.discount)

            if (product_price - discount) < 0 :
                return GraphQLError("Can't discount more than 100%")
            
            item_amount = (product_price - discount) * quantity
            
            vat_amount = (item_amount / 100) * Decimal(product.vat)
            total_amount += item_amount + vat_amount
            amount += item_amount
        return round(total_amount, 5),round(amount, 5) 
    def _restore_stock_and_delete_items(order):
        """Restore stock for existing order items and delete them."""
        existing_items = OrderProduct.objects.filter(order=order)
        for item in existing_items:
            # Restore stock for each ingredient
            ingredients = Ingredient.objects.filter(product=item.product)
            for ingredient in ingredients:
                ingredient.item.current_stock += ingredient.quantity * item.quantity
                ingredient.item.save()
                order_ingredient = OrderIngredients.objects.get(
                    order_product = item.id,
                    item = ingredient.item,
                )
                invoice_consumption = InvoiceConsumption.objects.get( order_ingredients_consumption=order_ingredient.id )
                invoice_consumption.purchase_invoice_item.quantity +=order_ingredient.quantity
                invoice_consumption.purchase_invoice_item.save()
                order_ingredient.delete()
                invoice_consumption.delete()


            # Delete the item from order
            item.delete()

    def _book_table(table_bookings, order):
        booking_expired()
        booked_tables = TableBooking.objects.filter(order=order.id)
        print(booked_tables)
        for table in booked_tables:
            

            table = FloorTable.objects.get(id=table.floor_table.id)
            
            table.is_booked = False
            table.save()
            booked_tables.delete()

        if not table_bookings:
            return

        table_bookings = json.loads(table_bookings) # [('table_id', 'duration_minutes')]
        # if table is not available, then return error
        for table_id, duration_minutes in table_bookings:
            table = FloorTable.objects.get(id=table_id, is_booked=False, is_active=True)
            if not table:
                raise GraphQLError(message="Table is already booked!")
                
        
        for table_id, duration_minutes in table_bookings:

            table = FloorTable.objects.get(id=table_id)

            TableBooking.objects.create(
                    floor_table=table,
                    order=order,
                    start_time=now(),
                    duration=timedelta(minutes=duration_minutes),
                    is_active=True
                )
            table.is_booked = True  # Mark table as booked
            table.save()

        release_expired_bookings.apply_async(
                    countdown=duration_minutes * 60          
                )
    

class OrderCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    order = graphene.Field(OrderType)
    
    class Meta:
        form_class = OrderForm

    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(Order, id=input.get('id'))
        
        form = OrderForm(input, instance=instance)
        if not input.get('order_id'):
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
            order_id = f"#{random_string}"
            input['order_id'] = order_id
        
        if not form.is_valid():
            return create_graphql_error(form) 
        
        
        # if order is already completed, then return error
        if instance and  (instance.status == ORDER_STATUS_CHOICES.COMPLETED or  instance.status == ORDER_STATUS_CHOICES.DUE):
            raise GraphQLError(message="Can not update order!")
        
        
        booking_expired()
        # if table is not available, then return error
        if input.get('table_bookings'):
            table_bookings = json.loads(input.get('table_bookings'))
            for table_id, duration_minutes in table_bookings:
                table = FloorTable.objects.get(id=table_id, is_booked=False, is_active=True)
                if not table:
                    raise GraphQLError(message="Table is already booked!")
        
        
            
                
        
        order = form.save()
        
        if input.get('table_bookings'):
            table_bookings = json.loads(input.get('table_bookings'))     # [('table_id', 'duration_minutes')]
            for table_id, duration_minutes in table_bookings:
                table = FloorTable.objects.get(id=table_id)
                TableBooking.objects.create(
                    floor_table=table,
                    order=order,
                    start_time=now(),
                    duration=timedelta(minutes=duration_minutes),
                    is_active=True
                )
                table.is_booked = True  # Mark table as booked
                table.save()
                task_result = release_expired_bookings.apply_async(
                    countdown=duration_minutes * 60          
                ) # countdown in seconds
        
        return OrderCUD(message="Created successfully!", success=True, order=order)
 

class OrderTypeUpdate(graphene.Mutation) :
    message = graphene.String()
    success = graphene.Boolean()    
    class Arguments:
        id = graphene.ID(required=True)
        orderType = graphene.String(required=True)
        
    
    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER])
    def mutate(self, info, id, orderType):
        order = get_object_by_kwargs(Order, {"id": id})
        if(order):
            order.type = orderType
            order.save()
        return OrderTypeUpdate(success=True, message="Success!")
    



class OrderProductCUD(DjangoFormMutation):
    success = graphene.Boolean()
    id = graphene.ID()
    class Meta:
        form_class = OrderProductForm

    def mutate_and_get_payload(self, info, **input):
        id=input.get('id')
        instance = get_object_or_none(OrderProduct, id=id)
        form = OrderProductForm(input, instance=instance)

        if not form.is_valid():
            return create_graphql_error(form)

        ingredients = Ingredient.objects.filter(product=input['product'])
        quantity = input['quantity']

        # for update 
        if id:
            order_product = OrderProduct.objects.get(id=id)
            pre_quantity = order_product.quantity
            for ingredient in ingredients:
                current_stock = ingredient.item.current_stock
                ingredient.item.current_stock = current_stock +  (pre_quantity * ingredient.quantity)
                ingredient.item.save()

        
        for ingredient in ingredients:
            current_stock = ingredient.item.current_stock
            ingredient.item.current_stock = current_stock -  (quantity * ingredient.quantity)
            ingredient.item.save()
      
        
        order = form.save()
        return OrderProductCUD( success=True, id=order.id)
        

class CheckIngredientAvailable(graphene.Mutation):
    success = graphene.Boolean() 
    message = graphene.String()

    class Arguments:
        order_products = graphene.List(graphene.NonNull(OrderProductInputType))
    
    def mutate(self, info, order_products):
        for item in order_products:
            ingredients =  Ingredient.objects.filter(product=item['product'])
            if ingredients.count():
                for ingredient in ingredients:
                    quantity  = item['quantity']
                    total_quantity = quantity * ingredient.quantity
                    current_stock = ingredient.item.current_stock
                    if (current_stock- total_quantity ) < 0:
                        return CheckIngredientAvailable(success=False,message=f"There is no enough {ingredient.item.name} in stock.")
        return CheckIngredientAvailable(success=True,message="Ingredients stock are enough")

class FloorCUD(DjangoFormMutation):
    success = graphene.Boolean()
    class Meta:
        form_class = FloorForm

    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(Floor, id=input.get('id'))
        form = FloorForm(input, instance=instance)
        if form.is_valid():
            order = form.save()
            return FloorCUD(success=True)
        create_graphql_error(form)

class FloorTableCUD(DjangoFormMutation):
    success = graphene.Boolean()
    class Meta:
        form_class = FloorTableForm

    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(FloorTable, id=input.get('id'))
        form = FloorTableForm(input, instance=instance)
        if form.is_valid():
            order = form.save()
            return FloorTableCUD( success=True)
        create_graphql_error(form)

class PaymentCUD(DjangoFormMutation):
    success = graphene.Boolean()
    message = graphene.String()
    payment = graphene.Field(PaymentType)
    class Meta:
        form_class = PaymentForm
    

    def mutate_and_get_payload(self, info, **input):
        try:
            instance = get_object_or_none(Payment, id=input.get('id'))
            form = PaymentForm(input, instance=instance)
            
            order = Order.objects.get(id=input.get('order'))

            final_amount = round(Decimal(order.final_amount), 4)
            amount = round(Decimal(input.get('amount')), 4)
            if final_amount < amount:
                raise GraphQLError(message="Payment amount is greater than order amount!")
            
            #  minimum payment amount is 1
            if amount < 1:
                raise GraphQLError(message="Payment amount should be greater than 1!")
            
            
            
            if not form.is_valid():
                create_graphql_error(form)
                
            
            # if order is already completed, then return error
            if order.status == ORDER_STATUS_CHOICES.COMPLETED:
                raise GraphQLError(message="Order is already completed!")
                
                
            # calculate total paid amount
            total_paid_amount = 0
            if order.payments :
                for payment in order.payments.all():
                    if payment.status == PAYMENT_STATUS_CHOICES.COMPLETED:
                        total_paid_amount += Decimal(payment.amount)
            
            # check if payment amount is greater than order amount
            if total_paid_amount + amount > final_amount:
                raise GraphQLError(message="Payment amount is greater than order amount!")
            
            # save payment
            newPayment  = form.save()
            

            total_paid_amount += amount
      
                
            # update order status
            if total_paid_amount >= final_amount:
                order.status = ORDER_STATUS_CHOICES.COMPLETED
                order.due = 0 # fully paid

            # update order status and due
            if total_paid_amount < final_amount:
                order.status = ORDER_STATUS_CHOICES.DUE
                order.due = final_amount - total_paid_amount
            
            
            
            
            # cart to order conversion 
            order.is_cart = False
            order.save()
            newPayment = Payment.objects.get(id=newPayment.id)
            return PaymentCUD(success=True, payment= newPayment,message="Payment successful!")
        except Exception as e:
            print(e)    
            raise GraphQLError(message="Payment failed!")
   

class DeleteOrderProduct(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()    
    class Arguments:
        id = graphene.ID(required=True)
    
    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER])
    def mutate(self, info, id):
        order_product = get_object_by_kwargs(OrderProduct, {"id": id})
        order_product.delete()
        return DeleteOrderProduct(success=True, message="Deleted!")
    
         
class DeleteIngredient(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()    
    class Arguments:
        id = graphene.ID(required=True)
    
    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER])
    def mutate(self, info, id):
        ingredient = get_object_by_kwargs(Ingredient, {"id": id})
        ingredient.delete()
        return DeleteIngredient(success=True, message="Deleted!")

class Mutation(graphene.ObjectType):
    product_cud = ProductCUD.Field()
    delete_product = DeleteProduct.Field()
    category_cud = CategoryCUD.Field()
    order_cud = OrderCUD.Field()
    order_product_cud = OrderProductCUD.Field()
    floor_cud = FloorCUD.Field()
    floor_table_cud = FloorTableCUD.Field()
    payment_cud = PaymentCUD.Field()
    delete_order_product = DeleteOrderProduct.Field()
    order_type_update = OrderTypeUpdate.Field()
    delete_ingredient = DeleteIngredient.Field()
    ingredient_cud = IngredientCUD.Field()
    check_ingredient_available = CheckIngredientAvailable.Field()
    order_cuv2 = OrderCUV2.Field()

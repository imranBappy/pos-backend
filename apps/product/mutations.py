import graphene
from apps.base.utils import get_object_or_none, generate_message, create_graphql_error
from apps.outlet.models import Outlet
from .objectType import CategoryType, ProductType, OrderProductType, OrderType, PaymentType
from apps.base.utils import get_object_by_kwargs
from backend.authentication import isAuthenticated

from apps.kitchen.models import Kitchen
from datetime import datetime
from graphene_django.forms.mutation import DjangoFormMutation
from .forms import ProductForm, CategoryForm, OrderForm, OrderProductForm, FloorForm, FloorTableForm, PaymentForm
from apps.product.models import Category,TableBooking, Product, Order,ORDER_STATUS_CHOICES,PAYMENT_STATUS_CHOICES, OrderProduct, Floor, FloorTable, Payment
from apps.accounts.models import Address, UserRole
import json 
from django.utils.timezone import now
from datetime import timedelta
from apps.product.tasks import release_expired_bookings, booking_expired
from graphql import GraphQLError
import random
import string
import uuid

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
        
        if form.is_valid()  == False:
            print(form.errors)
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
                if table == None:
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
        
    
    # @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER])
    def mutate(self, info, id, orderType):
        order = get_object_by_kwargs(Order, {"id": id})
        if(order):
            order.type = orderType
            order.save()
        return DeleteOrderProduct(success=True, message="Success!")
    
    
class OrderProductCUD(DjangoFormMutation):
    success = graphene.Boolean()
    id = graphene.ID()
    class Meta:
        form_class = OrderProductForm

    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(OrderProduct, id=input.get('id'))
        
        form = OrderProductForm(input, instance=instance)
        if form.is_valid():
            order = form.save()
            return OrderProductCUD( success=True, id=order.id)
        create_graphql_error(form)

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
            if order.final_amount < input.get('amount'):
                raise GraphQLError(message="Payment amount is greater than order amount!")
            
            #  minimum payment amount is 1
            if input.get('amount') < 1:
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
                        total_paid_amount += payment.amount
            
            # check if payment amount is greater than order amount
            if total_paid_amount + input.get('amount') > order.final_amount:
                raise GraphQLError(message="Payment amount is greater than order amount!")
            
            # save payment
            newPayment  = form.save()
            

            total_paid_amount += input.get('amount')
      
                
            # update order status
            if total_paid_amount >= order.final_amount:
                order.status = ORDER_STATUS_CHOICES.COMPLETED
                order.due = 0 # fully paid

            # update order status and due
            if total_paid_amount < order.final_amount:
                order.status = ORDER_STATUS_CHOICES.DUE
                order.due = order.final_amount - total_paid_amount
            
            
            
            
            # cart to order conversion 
            order.is_cart = False
            order.save()
            newPayment = Payment.objects.get(id=newPayment.id)
            return PaymentCUD(success=True, payment= newPayment,message="Payment successful!")
        except Exception as e:
            print(e)    
            raise GraphQLError(message="Payment failed!")
            


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
    
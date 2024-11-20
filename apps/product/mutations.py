import graphene
from apps.base.utils import get_object_or_none, generate_message, create_graphql_error
from .models import Category, Product
from apps.outlet.models import Outlet
from .objectType import CategoryType, ProductType
from apps.base.utils import get_object_by_kwargs

class CreateCategory(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        photo = graphene.String(required=True)
        description = graphene.String(required=True)

    def mutate(self, info, name, photo, description):
        new_category = Category(name=name, photo=photo, description=description)
        new_category.save()
        return CreateCategory(message="Success")


class UpdateCategory(graphene.Mutation):

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        photo = graphene.String()
        description = graphene.String()
    
    category = graphene.Field(CategoryType)

    def mutate(self, info,id, name=None, photo=None, description=None):
        category = get_object_by_kwargs(Category, {"id": id})
        if name is not None:
            category.name = name
        if photo is not None:
            category.photo = photo
        if description is not None:
            category.description = description
        category.save()
        return UpdateCategory(category=category)


class CreateProduct(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Int(required=True)
        description = graphene.String(required=True)
        photo = graphene.String(required=True)
        tax = graphene.Float(required=True)
        sku = graphene.String(required=True)
        cooking_time = graphene.Int(required=True)
        tag = graphene.String()

        category = graphene.ID()
        subcategory = graphene.ID(required=True)
        kitchen = graphene.ID(required=True)

    def mutate(self, info, name, price, description,
            photo,
            tax,
            sku,
            cooking_time,
            tag, 
            category, 
            subcategory, 
            kitchen
        ):
        find_category = get_object_by_kwargs(Category, {"id": category})
        find_subcategory = get_object_by_kwargs(Category, {"id": subcategory})
        find_kitchen = get_object_by_kwargs(Kitchen, {"id": kitchen})

        new_Product = Product(name=name, 
            price=price, 
            description=description, 
            photo=photo,
            tax=tax,
            sku=sku,
            cooking_time=cooking_time, 
            tag=tag, 
            category=find_category,
            subcategory=find_subcategory,
            kitchen=find_kitchen,
        )
        new_Product.save()
        return CreateProduct(message="Success")


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        photo = graphene.String()
        description = graphene.String()
        outlet = graphene.ID()
    
    product = graphene.Field(ProductType)

    def mutate(self, info,id, name=None, photo=None, description=None, outlet=None):
        product = get_object_by_kwargs(product, {"id": id})
        if name is not None:
            product.name = name
        if photo is not None:
            product.photo = photo
        if description is not None:
            product.description = description
        if outlet is not None:  
            find_outlet = get_object_by_kwargs(Outlet, {"id": outlet})
            product.outlet = find_outlet
        product.save()

        return UpdateProduct(Product=Product)

# class DeleteProduct(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID(required=True)
#     success = graphene.Boolean()
#     def mutate(self, info, id):
#         Product = get_object_by_kwargs(Product, {"id": id})
#         Product.delete()
#         return DeleteProduct(success=True)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
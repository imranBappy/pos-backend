import graphene
from apps.base.utils import get_object_or_none, generate_message, create_graphql_error
from .models import Kitchen
from apps.outlet.models import Outlet
from .objectType import KitchenType
from apps.base.utils import get_object_by_kwargs
from backend.authentication import isAuthenticated
class CreateKitchen(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()
    kitchen = graphene.Field(KitchenType)
    class Arguments:
        name = graphene.String(required=True)
        photo = graphene.String(required=True)
        description = graphene.String(required=True)
        outlet = graphene.ID(required=True)

    @isAuthenticated(['Manager', 'Admin'])
    def mutate(self, info, name, photo, description, outlet):
        find_outlet = get_object_by_kwargs(Outlet, {"id": outlet})
        new_kitchen = Kitchen(name=name, photo=photo, description=description, outlet=find_outlet)
        new_kitchen.save()
        return CreateKitchen(success = True,kitchen=new_kitchen, message="Success")



class UpdateKitchen(graphene.Mutation):

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        photo = graphene.String()
        description = graphene.String()
        outlet = graphene.ID()
    
    kitchen = graphene.Field(KitchenType)

    def mutate(self, info,id, name=None, photo=None, description=None, outlet=None):
        kitchen = get_object_by_kwargs(Kitchen, {"id": id})
        if name is not None:
            kitchen.name = name
        if photo is not None:
            kitchen.photo = photo
        if description is not None:
            kitchen.description = description
        if outlet is not None:  
            find_outlet = get_object_by_kwargs(Outlet, {"id": outlet})
            kitchen.outlet = find_outlet
        kitchen.save()

        return UpdateKitchen(kitchen=kitchen)

class DeleteKitchen(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        Kitchen = get_object_by_kwargs(Kitchen, {"id": id})
        Kitchen.delete()
        return DeleteKitchen(success=True)


class Mutation(graphene.ObjectType):
    create_Kitchen = CreateKitchen.Field()
    update_Kitchen = UpdateKitchen.Field()

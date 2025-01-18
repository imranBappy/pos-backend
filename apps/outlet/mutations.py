import graphene
from .inputObjectTypes import OutletInput
from .forms import OutletForm
from apps.base.utils import get_object_or_none, generate_message, create_graphql_error
from .models import Outlet
from .objectType import OutletType
from apps.base.utils import get_object_by_kwargs
from backend.authentication import isAuthenticated

class CreateOutlet(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()
    outlet = graphene.Field(OutletType)
    class Arguments:
        name = graphene.String(required=True)
        phone = graphene.String(required=True)
        email = graphene.String(required=True)
        address = graphene.String(required=True)

    
    @isAuthenticated(['ADMIN'])
    def mutate(self, info, name, phone, email, address):
        new_outlet = Outlet(name=name, phone=phone, email=email, address=address)
        new_outlet.save()
        return CreateOutlet(outlet=new_outlet,success=True, message="Outlet successfully created!")

class UpdateOutlet(graphene.Mutation):
    outlet = graphene.Field(OutletType)
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        phone = graphene.String()
        email = graphene.String()
        address = graphene.String()
    
    def mutate(self, info,id, name=None, phone=None, email=None, address=None):
        outlet = get_object_by_kwargs(Outlet, {"id": id})
        if name is not None:
            outlet.name = name
        if phone is not None:
            outlet.phone = phone
        if email is not None:
            outlet.email = email
        if address is not None:
            outlet.address = address
        outlet.save()

        return UpdateOutlet(outlet=outlet)

class DeleteOutlet(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        outlet = get_object_by_kwargs(Outlet, {"id": id})
        outlet.delete()
        return DeleteOutlet(success=True)


class Mutation(graphene.ObjectType):
    create_outlet = CreateOutlet.Field()
    update_outlet = UpdateOutlet.Field()

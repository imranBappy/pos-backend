import graphene
from .inputObjectTypes import OutletInput
from .forms import OutletForm
from apps.base.utils import get_object_or_none, generate_message, create_graphql_error
from .models import Outlet
from .objectType import OutletType
from apps.base.utils import get_object_by_kwargs
from backend.authentication import isAuthenticated
from graphene_django.forms.mutation import DjangoFormMutation

class CreateCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    outlet = graphene.Field(OutletType)
    class Meta:
        form_class = OutletForm
        
        

    
    @isAuthenticated()
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(Outlet, id=input.get('id'))
        form = OutletForm(input, instance=instance)
        if not form.is_valid():
            create_graphql_error(form)
            return
        
        new_outlet = form.save()
        return CreateCUD(outlet=new_outlet,success=True, message="Outlet successfully created!")

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
    outlet_cud = CreateCUD.Field()

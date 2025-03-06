import graphene
from apps.accounts.objectType import UserType, AddressType, RoleType, BuildingType
from graphene_django.filter import DjangoFilterConnectionField
from apps.accounts.models import User, Address, Building, UserRole
from apps.base.utils import  get_object_by_kwargs
from backend.authentication import isAuthenticated
from django.contrib.auth.models import Group
from graphene import Enum

class AddressTypeEnum(Enum):
    HOME = 'HOME'
    OFFICE = 'OFFICE'

class Query(graphene.ObjectType):
    users = DjangoFilterConnectionField(UserType)
    me = graphene.Field(UserType)
    user = graphene.Field(UserType,id=graphene.ID(required=False), email=graphene.String(required=False), phone=graphene.String(required=False))
    
    

    address = graphene.Field(AddressType, id=graphene.ID(required=False), user=graphene.ID(required=False), address_type=graphene.String(required=False))
    addresses = DjangoFilterConnectionField(AddressType)
    
    building = graphene.Field(BuildingType, id=graphene.ID(required=False), address=graphene.ID(required=False))
    buildings = DjangoFilterConnectionField(BuildingType)
    
    roles = graphene.List(RoleType)

    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER])
    def resolve_users(self, info,  **kwargs):
        return User.objects.all()
    
    @isAuthenticated()
    def resolve_me(self, info):
        user = info.context.User
        return user
    
    @isAuthenticated()
    def resolve_user(self, info, id=None, email=None, phone=None):
        try:
            if id:
                return User.objects.get(id=id)
            elif email:
                return User.objects.get(email=email)
            elif phone:
                return User.objects.get(phone=phone)
            raise User.DoesNotExist
        except User.DoesNotExist:
            raise Exception("User  not found.")
    
       
    def resolve_address(self, info, id=None, user=None, address_type=None):
        
        if id:
            return Address.objects.get(id=id)
        elif user and address_type:
            return Address.objects.get(user=user, address_type=address_type)
        return Address.objects.get(user=user )
    
    @isAuthenticated()
    def resolve_addresses(self, info, **kwargs):
        return Address.objects.all()
    @isAuthenticated()
    def resolve_building(self, info, id=None, address=None):
        if id:
            return get_object_by_kwargs(Building, {'id': id})
        elif address:
            return get_object_by_kwargs(Building, {'address': address})
        return get_object_by_kwargs(Building, { 'address':address, 'id':id })
    
    @isAuthenticated()
    def resolve_buildings(self, info, **kwargs):
        return Building.objects.all()
    @isAuthenticated()
    def resolve_roles(self, info, **kwargs):
        return Group.objects.all()


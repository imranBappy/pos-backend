import graphene
from graphene_django import DjangoObjectType
from .models import User, Address, Building
from .filters import UserFilter, AddressFilter, BuildingFilter
from backend.count_connection import CountConnection
from django.contrib.auth.models import Group
 

class UserType(DjangoObjectType):
    is_active = graphene.Boolean()   
    id = graphene.ID(required=True)
    class Meta:
        model = User
        fields = [
            'name', 'email', 'gender', 'date_of_birth', 'created_at','updated_at',
            'photo', 'role', 'phone', 'is_verified', 'term_and_condition_accepted',
            'privacy_policy_accepted', 'privacy_policy_accepted', 'is_active', 'address'
        ]
        filterset_class = UserFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection
    
    


class AddressType(DjangoObjectType):
    id = graphene.ID(required=True)
    class Meta:
        model = Address
        filterset_class = AddressFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection

class BuildingType(DjangoObjectType):
    id = graphene.ID(required=True)
    class Meta:
        model = Building
        filterset_class = BuildingFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection
 

class RoleType(DjangoObjectType):
    class Meta:
        model = Group
        

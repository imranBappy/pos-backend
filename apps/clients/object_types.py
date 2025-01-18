# at etzl/clients/schema.py

import graphene
from graphene_django import DjangoObjectType

from backend.count_connection import CountConnection

# local imports
from .filters import ClientDetailsFilters, ClientFilters
from .models import Client, ClientDetails


class ClientType(DjangoObjectType):
    """
        Define django object type for Client model with filter-set and relay node information
    """
    object_id = graphene.ID()

    class Meta:
        model = Client
        filterset_class = ClientFilters
        interfaces = (graphene.relay.Node,)
        convert_choices_to_enum = False
        connection_class = CountConnection

    @staticmethod
    def resolve_object_id(self, info, **kwargs):
        return self.pk


class ClientDetailsType(DjangoObjectType):
    """
        Define django object type for Client-details model with filter-set and relay node information
    """
    name = graphene.String()
    logo = graphene.String()
    cover_photo = graphene.String()

    class Meta:
        model = ClientDetails
        filterset_class = ClientDetailsFilters
        interfaces = (graphene.relay.Node,)
        convert_choices_to_enum = False
        connection_class = CountConnection

    @staticmethod
    def resolve_name(self, info, **kwargs):
        return self.client.name

    @staticmethod
    def resolve_logo(self, info, **kwargs):
        return self.logo_url

    @staticmethod
    def resolve_cover_photo(self, info, **kwargs):
        return self.cover_photo_url

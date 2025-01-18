import graphene
from graphene_django.types import DjangoObjectType
from .models import Outlet
from backend.count_connection import CountConnection
from .filters import OutletFilter


class OutletType(DjangoObjectType):
    id = graphene.ID(required=True)
    class Meta:
        model = Outlet
        fields = "__all__"
        filterset_class = OutletFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountConnection
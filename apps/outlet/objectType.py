from graphene_django.types import DjangoObjectType
import graphene
from .models import Outlet
from backend.count_connection import CountConnection
from .filters import OutletFilter


class OutletType(DjangoObjectType):
    id = graphene.ID(required=True)
    class Meta:
        model = Outlet
        fields = "__all__"
    def resolve_id(self, info):
        return self.id
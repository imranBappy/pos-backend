from graphene_django.types import DjangoObjectType
import graphene
from .models import Kitchen


class KitchenType(DjangoObjectType):
    id = graphene.ID(required=True)
    class Meta:
        model = Kitchen
        fields = "__all__"
    def resolve_id(self, info):
        return self.id
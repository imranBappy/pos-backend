import graphene

from .models import Kitchen, KitchenOrder, Printer
from apps.base.utils import get_object_by_kwargs
from .objectType import KitchenType, KitchenOrderType, PrinterType
from graphene_django.filter import DjangoFilterConnectionField
from apps.base.utils import get_object_by_id
 
from backend.authentication import isAuthenticated

class Query(graphene.ObjectType):
    kitchen = graphene.Field(KitchenType, id=graphene.ID(required=True))
    kitchens = DjangoFilterConnectionField(KitchenType)
    
    kitchenOrder  = graphene.Field(KitchenOrderType)
    kitchenOrders  = DjangoFilterConnectionField(KitchenOrderType)
    
    printer  = graphene.Field(PrinterType)
    printers  = DjangoFilterConnectionField(PrinterType)
    
    def resolve_kitchen(self, info, id):
        return get_object_by_kwargs(Kitchen, {"id": id})
    
    def resolve_kitchens(self, info,**kwargs):
        return Kitchen.objects.all()


    def resolve_kitchenOrder(self, info, id):
        return get_object_by_kwargs(KitchenOrder, {"id": id})
    
    def resolve_kitchenOrders(self, info ,**kwargs):
        return KitchenOrder.objects.all()


    def resolve_printer(self, info, id):
        return get_object_by_kwargs(Printer, {"id": id})
    
    def resolve_printers(self, info,**kwargs):
        return Printer.objects.all()
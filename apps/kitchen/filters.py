from .models import Kitchen, KitchenOrder, Printer
import django_filters as filters
from apps.base.filters import BaseFilterOrderBy


class KitchenFilter(BaseFilterOrderBy):
    name = filters.CharFilter(lookup_expr="icontains", field_name="name")
    class Meta:
        model = Kitchen
        fields = '__all__'

class KitchenOrderFilter(BaseFilterOrderBy):
    name = filters.CharFilter(lookup_expr="icontains", field_name="name")
    class Meta:
        model = KitchenOrder
        fields = '__all__'

class PrinterFilter(BaseFilterOrderBy):
    name = filters.CharFilter(lookup_expr="icontains", field_name="name")
    class Meta:
        model = Printer
        fields = '__all__'
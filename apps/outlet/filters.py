from .models import Outlet
import django_filters as filters
from apps.base.filters import BaseFilterOrderBy


class OutletFilter(BaseFilterOrderBy):
    name = filters.CharFilter(lookup_expr="icontains", field_name="name")
    class Meta:
        model = Outlet
        fields = ["id"]

import django_filters

from bases.filters import BaseFilters

from apps.clients.models import Client, ClientDetails


class ClientFilters(BaseFilters):
    """
        Client Filter will define here
    """
    id = django_filters.CharFilter(
        field_name='id',
        lookup_expr='exact'
    )

    class Meta:
        model = Client
        fields = [
            'id',
        ]


class ClientDetailsFilters(BaseFilters):
    """
        Client Filter will define here
    """
    id = django_filters.CharFilter(
        field_name='id',
        lookup_expr='exact'
    )

    class Meta:
        model = ClientDetails
        fields = [
            'id',
        ]

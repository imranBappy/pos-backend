from datetime import timedelta
from .models import User, Address, Building
import django_filters as filters
from apps.base.filters import BaseFilterOrderBy
from django.db.models import Q
from django.contrib.auth.models import Group

class UserFilter(BaseFilterOrderBy):
    name = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    role = filters.NumberFilter(lookup_expr="exact", field_name="role")
    is_verified = filters.BooleanFilter()
    is_active = filters.BooleanFilter()
    gender = filters.CharFilter(lookup_expr='exact')
    search = filters.CharFilter(method='filter_search')
    created_at_start = filters.DateFilter(method='filter_created_at_range', field_name='start')
    created_at_end = filters.DateFilter(method='filter_created_at_range', field_name='end')
    is_employee  = filters.BooleanFilter(method='filter_employee')
    is_staff  = filters.BooleanFilter(method='filter_staff')
    

    
    class Meta:
        model = User
        fields = [
            'name', 'email', 'gender', 'date_of_birth', 'created_at',
            'photo', 'role', 'phone', 'is_verified', 'term_and_condition_accepted',
            'privacy_policy_accepted', 'privacy_policy_accepted', 'is_active','is_staff'
        ]  
    
    def filter_staff(self, queryset, name, value):
        role = Group.objects.get(name="ADMIN")
        return queryset.filter(is_staff__exact=value).exclude(role=role.id)
    
    def filter_employee(self, queryset, name, value):
        return queryset.filter(role__name__in=['MANAGER','CHEF','WAITER'])


    
    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(email__icontains=value) | Q(phone__icontains=value)).order_by("name")
    

    def filter_created_at_range(self, queryset, name, value):
        if name == 'start':
            return queryset.filter(created_at__gte=value)
        if name == 'end':
            return queryset.filter(created_at__lte=value + timedelta(days=1))
        return queryset


class AddressFilter(BaseFilterOrderBy):
    user = filters.NumberFilter(lookup_expr="exact")
    addressType = filters.NumberFilter(lookup_expr="exact")
    
    
    class Meta:
        model = Address
        fields = '__all__'

class BuildingFilter(BaseFilterOrderBy):
    class Meta:
        model = Building
        fields = '__all__'      

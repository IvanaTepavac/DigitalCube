from django_filters import rest_framework as filters
from .models import Cities, Countries


class CitiesByFilters(filters.FilterSet):
    id = filters.NumberFilter(field_name="id", lookup_expr='exact')
    city = filters.CharFilter(field_name='city', lookup_expr='icontains')
    city_ascii = filters.CharFilter(field_name='city_ascii', lookup_expr='icontains')
    admin_name = filters.CharFilter(field_name='admin_name', lookup_expr='icontains')
    lat = filters.NumberFilter(field_name='lat', lookup_expr='exact')
    lng = filters.NumberFilter(field_name='lng', lookup_expr='exact')
    population = filters.RangeFilter(field_name='population')
    country = filters.NumberFilter(field_name='country', lookup_expr='exact')

    class Meta:
        model = Cities
        fields = ['id', 'city', 'city_ascii', 'admin_name', 'lat', 'lng', 'population', 'country']


class CountriesByFilters(filters.FilterSet):
    country_id = filters.NumberFilter(field_name='country_id', lookup_expr='exact')
    country = filters.CharFilter(field_name='country', lookup_expr='icontains')
    iso2 = filters.CharFilter(field_name='iso2', lookup_expr='icontains')
    iso3 = filters.CharFilter(field_name='iso3', lookup_expr='icontains')

    class Meta:
        model = Countries
        fields = ['country_id', 'country', 'iso2', 'iso3']

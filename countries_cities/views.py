from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from rest_framework.decorators import action

from .models import Cities, Countries, NearestCities
from .serializers import CitiesSerializer, CountriesSerializer, NearestCitiesSerializer, PopulationSerializer
from .filters import CitiesByFilters, CountriesByFilters


class CitiesList(generics.ListAPIView):
    """
    List of all Cities
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cities.objects.all()
    serializer_class = CitiesSerializer


class CityBy(viewsets.ModelViewSet):
    """
    Search Cities by filters
    All Cities in a particular Country
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cities.objects.all()
    serializer_class = CitiesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CitiesByFilters

    @action(methods=['get'], detail=False)
    def my_set(self, request):
        my_set = self.get_queryset()
        serializer = self.get_serializer_class()(my_set)
        return Response(serializer.data)


class CountriesList(generics.ListAPIView):
    """
    List of all Countries
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Countries.objects.all()
    serializer_class = CountriesSerializer


class CountryBy(viewsets.ModelViewSet):
    """
    Search Countries by filters
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Countries.objects.all()
    serializer_class = CountriesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CountriesByFilters

    @action(methods=['get'], detail=False)
    def my_set(self, request):
        my_set = self.get_queryset()
        serializer = self.get_serializer_class()(my_set)
        return Response(serializer.data)


class NearestCitiesList(viewsets.ModelViewSet):
    """
    Distance of Cities for the selected Country
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NearestCitiesSerializer

    def list(self, request, *args, **kwargs):
        country_id = int(kwargs['country_id'])
        country_cities = list(Cities.objects.filter(country=country_id))
        ncities = NearestCities.nearestcities(country_cities)
        nearest_serializer = NearestCitiesSerializer(ncities[0])
        furthest_serializer = NearestCitiesSerializer(ncities[1])
        return Response({'nearest': nearest_serializer.data, 'furthest': furthest_serializer.data})


class Compass(viewsets.ModelViewSet):
    """
    Northernmost, easternmost, southernmost, and westernmost cities for the selected country
    and  their distance from each other
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        country_id = int(kwargs['country_id'])
        country_cities = list(Cities.objects.filter(country=country_id))
        northest = max(country_cities, key=lambda x: x.lat)
        southest = min(country_cities, key=lambda x: x.lat)
        eastest = max(country_cities, key=lambda x: x.lng)
        westest = min(country_cities, key=lambda x: x.lng)

        north_ser = CitiesSerializer(northest)
        south_ser = CitiesSerializer(southest)
        east_ser = CitiesSerializer(eastest)
        west_ser = CitiesSerializer(westest)

        return Response(
            {'northest': north_ser.data,
             'southest': south_ser.data,
             'eastest': east_ser.data,
             'westest': west_ser.data,
             'northest-southest dist': Cities.city_dist(northest, southest),
             'northest-eastest dist': Cities.city_dist(northest, eastest),
             'northest-westest dist': Cities.city_dist(northest, westest),
             'southest-eastest dist': Cities.city_dist(southest, eastest),
             'southest-westest dist': Cities.city_dist(southest, westest),
             'eastest-westest dist': Cities.city_dist(eastest, westest),
             })


class Population(viewsets.ModelViewSet):
    """
    City with the largest/smallest population for the set of selected countries
    and total number of residents in all cities for each country in the set
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PopulationSerializer

    def list(self, request, *args, **kwargs):
        params = kwargs['country_id']
        country_ids = list(map(int, params.split(',')))
        cities_population = list(Cities.objects.filter(country_id__in=country_ids).order_by('population'))
        largest_serializer = PopulationSerializer(cities_population[-1])
        smallest_serializer = PopulationSerializer(cities_population[0])
        totpop_dict = Cities.objects.filter(country_id__in=country_ids).values('country_id').order_by('country_id')\
            .annotate(total_population=Sum('population'))

        return Response(
            {'largest': largest_serializer.data,
             'smallest': smallest_serializer.data,
             'total population': totpop_dict
             })

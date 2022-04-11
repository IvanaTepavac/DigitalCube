from rest_framework import serializers

from .models import Cities, Countries, NearestCities


class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ('id', 'city', 'city_ascii', 'admin_name', 'lat', 'lng', 'population', 'country')


class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = ('country_id', 'country', 'iso2', 'iso3')


class NearestCitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NearestCities
        fields = ('city1', 'city2', 'dist')


class PopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ('city', 'population', 'country')

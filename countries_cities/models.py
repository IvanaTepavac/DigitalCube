from django.db import models
from math import radians, cos, sin, asin, sqrt


class Countries(models.Model):
    country_id = models.BigAutoField(primary_key=True)
    country = models.CharField('country', max_length=100)
    iso2 = models.CharField('ISO2', max_length=20)
    iso3 = models.CharField('ISO3', max_length=20)

    @property
    def city_name(self):
        """
        Return field 'city_name' for serializers
        """
        return self.city.city

    def __str__(self):
        return self.country


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


class Cities(models.Model):
    id = models.BigAutoField(primary_key=True)
    city = models.CharField('City', max_length=50)
    city_ascii = models.CharField('City ASCII', max_length=50)
    admin_name = models.CharField('Administration Name', max_length=50)
    lat = models.FloatField('Latitude', default=0)
    lng = models.FloatField('Longitude', default=0)
    population = models.CharField('Population', max_length=15)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, db_column='country')

    def __str__(self):
        return self.city

    @staticmethod
    def city_dist(city1, city2):
        return haversine(city1.lng, city1.lat, city2.lng, city2.lat)


class NearestCities(models.Model):
    city1 = models.CharField('City1', max_length=50)
    city2 = models.CharField('City2', max_length=50)
    dist = models.FloatField('Latitude', default=0)

    @staticmethod
    def nearestcities(cities):
        maxdist = 0
        maxpair = ()
        mindist = 1e9
        minpair = ()
        for city1 in cities:
            for city2 in cities:
                if city1 == city2:
                    continue

                dist = Cities.city_dist(city1, city2)
                if maxdist < dist:
                    maxdist = dist
                    maxpair = (city1, city2)

                if mindist > dist:
                    mindist = dist
                    minpair = (city1, city2)

        nearest = NearestCities()
        nearest.dist = mindist
        nearest.city1 = minpair[0].city
        nearest.city2 = minpair[1].city

        furthest = NearestCities()
        furthest.dist = maxdist
        furthest.city1 = maxpair[0].city
        furthest.city2 = maxpair[1].city

        return [nearest, furthest]

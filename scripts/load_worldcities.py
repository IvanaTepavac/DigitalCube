import csv
from django.apps import apps

Cities = apps.get_model('countries_cities', 'Cities')
Countries = apps.get_model('countries_cities', 'Countries')


def run():
    with open('scripts/worldcities.csv') as file:
        reader = csv.reader(file)
        next(reader)

        Cities.objects.all().delete()
        Countries.objects.all().delete()
        country_names = {}

        for row in reader:
            print(row)
            country_name = row[4]
            if country_name not in country_names:
                country = Countries(country=row[4],
                                    iso2=row[5],
                                    iso3=row[6],
                                    )
                country.save()
                country_names[country_name] = country

            country = country_names[country_name]

            city, _ = Cities.objects.get_or_create(id=row[-1],
                                                   city=row[0],
                                                   city_ascii=row[1],
                                                   admin_name=row[7],
                                                   lat=row[2],
                                                   lng=row[3],
                                                   population=row[9],
                                                   country=country
                                                   )
            city.save()



GEOGRAPHY

is a project for managing geolocation data, with multiple HTTP REST API routes

CONSIST OF TWO APPS:

users: for users’ registration, login and obtaining an authorization token.
countries_cities: to store and obtain data on countries and their cities.

INSTALLATION:

project build: pip install django,
               pip install djangorestframework,
               pip install djangorestframework-simplejwt

db populating: csv file from https://simplemaps.com/data/world-cities

The CSV file contains data about countries,
cities, population, and geolocations of those cities.

scripts: contains load_worldcities.py file to import rows for models tables Cities and Countries. 
         Command(terminal): python manage.py runscript load_worldcities

filters: pip install django-filter
         To search by parameters.

API ENDPOINTS:

'register/'  - user registration

'api/token/'  - login, returns token

'users/'  - list of all users

'users/<int:id>'  - user detail, editing by id

'cities/'  - list of all cities

'city-by/'  - search cities by filters, all cities in a particular country

'countries/'  - list of all countries

'county-by/'  - search countries by filters

'task-a/<int:country_id>'  - distance of cities

'task-c/<int:country_id>'  - cities geolocation and mutual distance

'task-d/<str:country_id>'  - cities/country population
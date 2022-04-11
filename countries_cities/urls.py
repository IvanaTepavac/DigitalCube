from django.urls import path
from . import views


urlpatterns = [
    path('cities/', views.CitiesList.as_view(), name='cities'),
    path('city-by/', views.CityBy.as_view({'get': 'list'}), name='city_by'),
    path('countries/', views.CountriesList.as_view(), name='countries'),
    path('country-by/', views.CountryBy.as_view({'get': 'list'}), name='country_by'),
    path('task-a/<int:country_id>', views.NearestCitiesList.as_view({'get': 'list'}), name='task_a'),
    path('task-c/<int:country_id>', views.Compass.as_view({'get': 'list'}), name='task_c'),
    path('task-d/<str:country_id>', views.Population.as_view({'get': 'list'}), name='task_d'),
]

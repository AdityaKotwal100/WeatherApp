from django.urls import path
from . import views
urlpatterns = [
    #Home page
    path('',views.index,name = "home"),
    #Delete city route
    path('delete/<city_name>/',views.delete_city,name='delete_city'),
    #More information on the selected city
    path('more_info/<city_name>/',views.weather_forecast,name='weather_forecast')

]

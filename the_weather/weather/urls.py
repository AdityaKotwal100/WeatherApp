from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name = "home"),
    path('delete/<city_name>/',views.delete_city,name='delete_city'),
    path('more_info/<city_name>/',views.weather_forecast,name='weather_forecast')

]

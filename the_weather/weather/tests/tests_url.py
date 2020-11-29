from django.test import SimpleTestCase
from django.urls import reverse, resolve
from weather.views import index, delete_city, weather_forecast


class TestUrls(SimpleTestCase):

    #Tests for Index function, i.e. Homepage
    def test_index_url_is_resolved(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)
    
    #Tests for Delete function
    def test_delete_city_url_is_resolved(self):
        url = reverse('delete_city',args=['some-city'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, delete_city)
    
    #Tests for More information page.
    def test_weather_forecast_url_is_resolved(self):
        url = reverse('weather_forecast', args=['some-city'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, weather_forecast)
        
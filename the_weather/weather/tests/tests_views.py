from django.test import TestCase, Client
from django.urls import reverse
from weather.models import City
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.delete_url = reverse('delete_city',args = ['some_city'])
        self.more_info_url = reverse('weather_forecast',args = ['some_city'])
        self.some_city = City.objects.create(
            name = 'some_city'
        )

    def test_index_GET(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,('weather/weather.html'))
    
    def test_delete_city(self):
        response = self.client.get(self.delete_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,('weather/weather.html'))
    
    def test_more_info_GET(self):
        response = self.client.get(self.more_info_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,('weather/forecast.html'))
    
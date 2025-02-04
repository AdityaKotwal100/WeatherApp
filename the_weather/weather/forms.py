from django.forms import ModelForm, TextInput
from .models import City

#Form to add new city to Homepage
class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name' : TextInput(attrs={'autocomplete': 'off', 'class' : 'input' , 'placeholder' : 'City Name'})}
    
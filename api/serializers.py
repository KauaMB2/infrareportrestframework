from rest_framework import serializers
from .models import Occurrence, Citizen, City 

class OccurrenceSerializer(serializers.ModelSerializer):#Class to serialize
    class Meta:
        model = Occurrence#Define the class(table)
        fields = '__all__'#Define the colums that will be serialized
class CitizenSerializer(serializers.ModelSerializer):#Class to serialize
    class Meta:
        model = Citizen#Define the class(table)
        fields = '__all__'#Define the colums that will be serialized
class CitySerializer(serializers.ModelSerializer):#Class to serialize
    class Meta:
        model = City#Define the class(table)
        fields = '__all__'#Define the colums that will be serialized
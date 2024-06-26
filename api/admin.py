from django.contrib import admin
from .models import Occurrence, Citizen, City
# Register your models here.
admin.site.register(Occurrence)#it allow the admin modify informations about the intance
admin.site.register(Citizen)#it allow the admin modify informations about the intance
admin.site.register(City)#it allow the admin modify informations about the intance
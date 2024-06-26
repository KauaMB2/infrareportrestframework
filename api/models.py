from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
class Occurrence(models.Model):
    citizen_email = models.EmailField(unique=False, null=True)
    occurrence_type = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    user_comment = models.TextField(max_length=1000)
    cep=models.IntegerField(null=True)
    concluded=models.CharField(default="Em aberto", null=False, max_length=10)
    city_comment=models.CharField(default="", null=False, max_length=1000)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    image = models.ImageField(upload_to="occurrences/", null=True, default="occurrences/occurrenceVoid.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.occurrence_type} - {self.created_at}"

class Citizen(models.Model):
    citizen_name = models.CharField(max_length=100)
    cep=models.IntegerField(null=True)
    state_name = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    residential_number = models.TextField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=200)
    points=models.IntegerField(default=50,validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.citizen_name

class City(models.Model):
    city_name = models.CharField(max_length=100)
    state_name = models.CharField(max_length=100)
    cep=models.IntegerField(null=True)
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.city_name
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Location(models.Model):
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=5)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f'{self.city}, {self.state} {self.zip_code}'


class Truck(models.Model):
    number = models.CharField(max_length=5, unique=True)
    current_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    carrying_capacity = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(1000)
    ])

    def __str__(self):
        return self.number


class Cargo(models.Model):
    pick_up_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pick_up_cargos')
    delivery_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='delivery_cargos')
    weight = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(1000)
    ])
    description = models.TextField()

    def __str__(self):
        return f'Cargo #{self.pk}'

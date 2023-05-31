from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from cargo_logistics.models import Truck, Cargo
from geopy.distance import distance


class CargoCreateSerializer(serializers.Serializer):
    pick_up_zip = serializers.CharField(max_length=5)
    delivery_zip = serializers.CharField(max_length=5)
    weight = serializers.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(1000)
    ])
    description = serializers.CharField()



class CargoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['id', 'weight', 'description']


class CargoListSerializer(serializers.ModelSerializer):
    nearest_trucks = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ['id', 'pick_up_location', 'delivery_location', 'nearest_trucks']

    @staticmethod
    def get_nearest_trucks(cargo):
        cargo_latitude = cargo.pick_up_location.latitude
        cargo_longitude = cargo.pick_up_location.longitude
        cargo_location = (cargo_latitude, cargo_longitude)
        trucks_queryset = Truck.objects.all()
        trucks_locations = {
            truck.pk: (truck.current_location.latitude, truck.current_location.longitude) for truck in trucks_queryset
        }
        nearest_trucks = [
            truck_id for truck_id, truck_location in trucks_locations.items() if
            int(distance(cargo_location, truck_location).mi) < 450
        ]
        return nearest_trucks


class CargoDetailSerializer(serializers.ModelSerializer):
    trucks = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ['id', 'pick_up_location', 'delivery_location', 'weight', 'description', 'trucks']

    def get_trucks(self, cargo):
        all_trucks = Truck.objects.all()
        trucks = [
            {
                'truck': truck.number,
                'distance': int(distance(
                    (cargo.pick_up_location.latitude, cargo.pick_up_location.longitude),
                    (truck.current_location.latitude, truck.current_location.longitude)
                ).mi)
            }
            for truck in all_trucks
        ]
        return trucks


class TruckSerializer(serializers.Serializer):
    location_zip = serializers.CharField(max_length=5)


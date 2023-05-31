from django.contrib import admin
from cargo_logistics.models import Cargo, Location, Truck


admin.site.register(Cargo)
admin.site.register(Location)
admin.site.register(Truck)

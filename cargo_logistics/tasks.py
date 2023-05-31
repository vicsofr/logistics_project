from sys import stdout

from celery import shared_task
from .models import Truck, Location


@shared_task
def update_truck_locations():
    trucks = Truck.objects.all()
    trucks_to_update = []
    for truck in trucks:
        random_location = Location.objects.order_by('?').first()
        truck.current_location = random_location
        trucks_to_update.append(truck)
    Truck.objects.bulk_update(trucks_to_update, ['current_location'])
    stdout.write(f'{len(trucks_to_update)} locations of Truck objects were rewritten')

from django.core.management.base import BaseCommand
from cargo_logistics.models import Location, Truck
import csv
import random
import string


class Command(BaseCommand):
    help = 'Creates initial database records'

    def handle(self, *args, **options):
        if Location.objects.exists() or Truck.objects.exists():
            self.stdout.write(self.style.NOTICE('Database records already exist. Skipping creation.'))
            return

        with open('load_data/uszips.csv', 'r') as file:
            reader = csv.DictReader(file)
            locations = [
                Location(
                    city=row['city'],
                    state=row['state_id'],
                    zip_code=row['zip'],
                    latitude=float(row['lat']),
                    longitude=float(row['lng'])
                )
                for row in reader
            ]
            Location.objects.bulk_create(locations)

        def generate_unique_number():
            number = random.randint(1000, 9999)
            letter = random.choice(string.ascii_uppercase)
            return f'{number}{letter}'

        for _ in range(20):
            car = Truck(
                number=generate_unique_number(),
                current_location=random.choice(Location.objects.all()),
                carrying_capacity=random.randint(1, 1000)
            )
            car.save()

        self.stdout.write(self.style.SUCCESS('Database records created successfully.'))

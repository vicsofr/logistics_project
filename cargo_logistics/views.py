from rest_framework import generics, status
from rest_framework.response import Response

from .models import Location, Truck, Cargo
from .serializers import (
    CargoDetailSerializer, CargoCreateSerializer, TruckSerializer, CargoListSerializer, CargoUpdateSerializer
)


class CargoCreateAPIView(generics.CreateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoCreateSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            pick_up_zip = serializer.validated_data.get('pick_up_zip')
            delivery_zip = serializer.validated_data.get('delivery_zip')

            try:
                pick_up_location = Location.objects.get(zip_code=pick_up_zip)
                delivery_location = Location.objects.get(zip_code=delivery_zip)
            except Location.DoesNotExist:
                return Response({'error': 'Invalid zip code'}, status=status.HTTP_400_BAD_REQUEST)

            cargo = Cargo.objects.create(
                pick_up_location=pick_up_location,
                delivery_location=delivery_location,
                weight=serializer.validated_data.get('weight'),
                description=serializer.validated_data.get('description')
            )

            return Response(
                {
                    'status': 'success',
                    'created': f'{cargo.__str__()}'
                }, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CargoListAPIView(generics.ListAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoListSerializer
    http_method_names = ['get']


class CargoDetailAPIView(generics.RetrieveAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoDetailSerializer
    lookup_field = 'pk'
    http_method_names = ['get']


class CargoUpdateAPIView(generics.UpdateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoUpdateSerializer
    lookup_field = 'pk'
    http_method_names = ['put']


class CargoDestroyAPIView(generics.DestroyAPIView):
    queryset = Cargo.objects.all()
    lookup_field = 'pk'
    http_method_names = ['delete']

    def destroy(self, request, *args, **kwargs):
        cargo = self.get_object()
        cargo_object_name = cargo.__str__()
        cargo.delete()

        return Response(
            {'success': f'{cargo_object_name} was deleted'},
            status=status.HTTP_200_OK
        )


class TruckUpdateAPIView(generics.UpdateAPIView):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    lookup_field = 'pk'
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        truck = self.get_object()
        location_zip = request.data.get('location_zip')

        try:
            location = Location.objects.get(zip_code=location_zip)
        except Location.DoesNotExist:
            return Response({'error': f'Invalid zip code {location_zip}'}, status=status.HTTP_400_BAD_REQUEST)

        truck.current_location = location
        truck.save()

        return Response(
            {'success': f'Truck #{truck.number} saved with location "{location.__str__()}"'},
            status=status.HTTP_200_OK
        )

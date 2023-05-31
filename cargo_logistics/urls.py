from django.urls import path
from cargo_logistics.views import (
    CargoCreateAPIView, CargoListAPIView, CargoDetailAPIView, CargoUpdateAPIView, CargoDestroyAPIView,
    TruckUpdateAPIView
)

urlpatterns = [
    path('cargos/', CargoListAPIView.as_view(), name='cargo-list'),
    path('cargos/create/', CargoCreateAPIView.as_view(), name='cargo-create'),
    path('cargos/<int:pk>/', CargoDetailAPIView.as_view(), name='cargo-detail'),
    path('cargos/<int:pk>/update/', CargoUpdateAPIView.as_view(), name='cargo-update'),
    path('cargos/<int:pk>/destroy/', CargoDestroyAPIView.as_view(), name='cargo-destroy'),
    path('trucks/<int:pk>/update/', TruckUpdateAPIView.as_view(), name='truck-update'),
]

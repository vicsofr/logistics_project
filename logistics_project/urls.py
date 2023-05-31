from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('logistics/', include('cargo_logistics.urls')),
    path('admin/', admin.site.urls),
]

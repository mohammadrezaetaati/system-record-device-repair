from django.urls import path

from .views import EditPlace


urlpatterns = [
    path("edit/", EditPlace.as_view(), name="device-all"),
]

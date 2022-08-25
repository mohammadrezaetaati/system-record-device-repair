from django.urls import path

from .views import SeeAllDevice, CheckSerial, AddDevice

urlpatterns = [
    path("device-all/", SeeAllDevice.as_view(), name="device-all"),
    path("check-serial/", CheckSerial.as_view(), name="check-serial"),
    path("add-device/", AddDevice.as_view(), name="add-device"),
    path("edit-status/", CheckSerial.as_view(), name="edit-status"),
]

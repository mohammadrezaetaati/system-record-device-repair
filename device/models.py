from datetime import datetime

from django.db import models
from django.conf import settings


import device.function


class Category(models.Model):
    name = models.CharField(max_length=255)


class Device(models.Model):

    STATUS_CHOICES = [
        ("ongoing", "دردست اقدام"), ("finished", "آماده به تحویل")
    ]

    work_order_number = models.CharField(max_length=30)
    serial = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    entry_date = models.CharField(max_length=20, editable=False)
    exit_date = models.DateTimeField(null=True, blank=True)
    transferee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    delivery = models.CharField(max_length=255, null=True, blank=True)
    problem = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(
        max_length=255, null=True, blank=True, default=" "
    )
    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default="دردست اقدام"
    )

    def save(self, *args, **kwargs):

        time = datetime.now()
        time_now = time.time().strftime("%H:%M:%S")
        self.entry_date = f"{ time_now} {device.functions.g_to_p()}"
        super(Device, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.work_order_number


class Place(models.Model):
    name = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    boss = models.CharField(max_length=255)


class Parts(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    parts_install = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    data_time = models.DateTimeField()

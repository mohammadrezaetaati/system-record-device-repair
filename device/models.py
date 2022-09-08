from datetime import datetime
from unicodedata import category


from django.db import models
from django.conf import settings


import device.functions
from place.models import Branch,Place








class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class BrandCategory(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    

    def __str__(self) -> str:
        return f'{self.name}-{self.category.name}'


class Part(models.Model):
    device=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    brand=models.CharField(max_length=100)
    amount=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return f'{self.device}-{self.name}'


class Input(models.Model):

    STATUS_CHOICES = [
        ("ngoing", "دردست اقدام"), ("finished", "آماده به تحویل")
    ]

    work_order_number = models.CharField(max_length=30)
    serial = models.CharField(max_length=255)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand_category=models.ForeignKey(BrandCategory,on_delete=models.CASCADE)
    place = models.ForeignKey(Place,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    entry_date = models.CharField(max_length=20, editable=False)
    exit_date = models.DateTimeField(null=True, blank=True)
    transferee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    parts=models.ManyToManyField(Part,null=True,blank=True)
    problem = models.CharField(max_length=255)
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
        super(Input, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.work_order_number






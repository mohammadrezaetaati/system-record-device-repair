from datetime import datetime





from django.db import models
from django.core.validators import RegexValidator


import device.functions
from place.models import Branch,Place








class Category(models.Model):
    name=models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name

class BrandCategory(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    

    def __str__(self) -> str:
        return f'{self.name}-{self.category.name}'

class Part(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    brand=models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f'{self.name}-{self.brand}'

    class Meta:
        ordering=('category__name','name','brand',)
      
        
        
class NumberPart(models.Model):
    number=models.SmallIntegerField(default=1)
    part=models.ForeignKey(Part,on_delete=models.PROTECT,null=True,blank=True)

    # def __str__(self) -> str:
        # return 

class DeviceRequest(models.Model):

    STATUS_CHOICES = [
        ('confirmation','Confirmation'),
        ('waiting','Waiting'),
        ('cancel','Cancel'),
    ]
    
   
    status = models.CharField(max_length=12,choices=STATUS_CHOICES)



class DeviceInput(models.Model):

    STATUS_CHOICES = [
        ("unrepairable", "غیرقابل تعمیر"),
        ('finished','تحویل داده شده'),
        ("provide", "آماده به تحویل"),
        ("repair_city", "تعمیردرشهر"),
        ("ngoing", "دردست اقدام"), 
        ('waiting','Waiting'),
        ('cancel','Cancel'),
    ]
    work_order_number = models.CharField(max_length=30,validators=[RegexValidator(regex='^[1۱][3-9۳-۹][0-9۰-۹][0-9۰-۹]\/[1-9۱-۹]{1}[0-9۰-۹]*$')])
    serial = models.CharField(max_length=10,validators=[RegexValidator(regex='^[0-9۰-۹]{2,10}$')])
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    brand_category = models.ForeignKey(BrandCategory,on_delete=models.PROTECT)
    place = models.ForeignKey(Place,on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch,on_delete=models.PROTECT)
    request_date = models.DateTimeField(null=True,blank=True)
    entry_date = models.DateTimeField(null=True,blank=True)
    exit_date = models.DateTimeField(null=True,blank=True)
    provide_date = models.DateTimeField(null=True,blank=True)
    repair_city_date = models.DateTimeField(null=True,blank=True)
    delivery = models.CharField(max_length=30,validators=[RegexValidator(regex='^[ا-ی\s]{3,30}$')])
    delivery_operator = models.CharField(max_length=100,null=True,blank=True,default='-')
    transferee = models.CharField(max_length=30,null=True,blank=True,default='-')
    transferee_operator = models.CharField(max_length=100)
    seal_number = models.CharField(max_length=30,null=True,blank=True,default='-')
    parts = models.ManyToManyField(NumberPart,null=True,blank=True,default='-')
    problem = models.CharField(max_length=255)
    description_cancel = models.CharField(max_length =100,null=True,blank=True)
    description = models.CharField(
        max_length=255, null=True, blank=True, default="-"
    )
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES
    )

    def __str__(self) -> str:
        return self.work_order_number

    class Meta:
        ordering=('-entry_date',)




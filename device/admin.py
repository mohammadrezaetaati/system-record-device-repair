from django.contrib import admin

from .models import Parts, Device, Place, Category


admin.site.register(Parts)
admin.site.register(Device)
admin.site.register(Place)
admin.site.register(Category)

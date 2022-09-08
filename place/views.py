from django.shortcuts import render

from device.views import EditCategory
from .models import Place

class EditPlace(EditCategory):

    def get(self, request):
        return render(request,'place/form_edit_place.html')
        

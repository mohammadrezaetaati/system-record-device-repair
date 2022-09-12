import json
from typing import Union,List,Type

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet,Model


from device.views import EditCategory
from .models import Place
from .forms import PlaceForm

class EditPlace(EditCategory):
    place_id=None
 
    def get(self, request):
        places=Place.objects.all()
        return render(request,'place/form_edit_place.html',context={'places':places})

    def ajax_edit(request):
        EditPlace.place_id=request.GET.get('place_id')
        place:Place=get_object_or_404(Place,id=int(EditPlace.place_id))
        return JsonResponse({'name':place.name,'boss':place.boss})

    def ajax_delete(request):
        place_id=request.GET.get('place_id')
        place:Place=get_object_or_404(Place,id=int(place_id))
        place.delete()
        return JsonResponse({'msg':'success'})

    def create(self, data: dict, model: type[Model]) -> json:
        if self.obj_exists(name=data['name'],queryset=model):
                return self.response('exists')
        model.objects.create(**data)
        return self.response('success')

    def post(self, request):
        form=PlaceForm(request.POST)
        if form.is_valid():
            if 'form_add' in form.data:
                return self.create(model=Place,data=form.cleaned_data)
            else:
                Place.objects.filter(id=int(EditPlace.place_id)).update(**form.cleaned_data)
                return JsonResponse({'msg':'update'})
        else:
                return JsonResponse({'msg':'error'})


       
        



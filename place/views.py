import json
from persian import convert_en_numbers
from typing import Union,List,Type
from unicodedata import name

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet,Model
from django.views import View
from django.db.models import ProtectedError

from device.views import EditCategory
from .models import Place,Branch
from .forms import PlaceForm,Branchform

class EditPlace(View):
    place_id=None
    place=None

    def get(self, request):
        places=Place.objects.all()
        return render(request,'place/form_edit_place.html',context={'places':places})

    def load_data_ajax(request):
        EditPlace.place_id=request.GET.get('place_id')
        EditPlace.place:Place=get_object_or_404(Place,id=int(EditPlace.place_id))
        return JsonResponse({'name':EditPlace.place.name,'boss':EditPlace.place.boss})

    def ajax_delete(request):
        place_id=request.GET.get('place_id')
        place:Place=get_object_or_404(Place,id=int(place_id))
        try:
            place.delete()
        except ProtectedError:
            return JsonResponse({'msg':'protectederror'})
        return JsonResponse({'msg':'success'})

    def obj_exists(self, name: str) -> bool:
        return Place.objects.filter(name=name).exists()
    
    def create(self, data: dict) -> json:
        if self.obj_exists(name=data['name']):
            return JsonResponse({'msg':'exists'})
        Place.objects.create(**data)
        return JsonResponse({'msg':'success'})

    def update(self, data:dict) -> json:
        if EditPlace.place.name != data['name']:
            if self.obj_exists(name=data['name']):
                return JsonResponse({'msg':'exists'})
        Place.objects.filter(id=int(EditPlace.place_id)).update(**data)
        return JsonResponse({'msg':'success'})

    def post(self, request):
        form=PlaceForm(request.POST)
        if form.is_valid():
            if 'form_add' in form.data:
                return self.create(data=form.cleaned_data)
            else:
                return self.update(data=form.cleaned_data)
        else:
                return JsonResponse({'msg':'error'})


class EditBranch(View):
    branch_id=None
    branch=None

    def get(self,request):
        branchs=Branch.objects.all()
        places=Place.objects.all()
        context={
            'branchs':branchs,
            'places':places
        }
        return render(request,'place/form_edit_branch.html',context=context)      

    def obj_exists(self, data:dict) -> bool:
        return Branch.objects.filter(name=data['name'],place=data['place']).exists()

    def create(self, data: dict) -> json:
        if self.obj_exists(data):
            return JsonResponse({'msg':'exists'})
        Branch.objects.create(phone=convert_en_numbers(data.pop('phone')),**data)
        return JsonResponse({'msg':'success'})

    def update(self, data:dict) -> json:
        place=data['place']
        print(EditBranch.branch.place.name)
        # print(data['place'].name !=EditBranch.branch.place.name)
        if EditBranch.branch.name != data['name'] or EditBranch.branch.place.name != place.name:
            if self.obj_exists(data):
                return JsonResponse({'msg':'exists'})
        Branch.objects.filter(id=int(EditBranch.branch_id)).update(**data)
        return JsonResponse({'msg':'success'})  

    def load_data_ajax(request):
        EditBranch.branch_id=request.GET.get('branch_id')
        EditBranch.branch:Branch=get_object_or_404(Branch,id=int(EditBranch.branch_id))
        return JsonResponse({
                'name':EditBranch.branch.name,
                'boss':EditBranch.branch.boss,
                'place':EditBranch.branch.place.name,
                'place_id':EditBranch.branch.place.id,
                'phone':EditBranch.branch.phone,
            })

    def ajax_delete(request):
        branch_id=request.GET.get('branch_id')
        branch:Branch=get_object_or_404(Branch,id=int(branch_id))
        branch.delete()
        return JsonResponse({'msg':'success'})

    def post(self,request):
        form=Branchform(request.POST)
        if form.is_valid():
            if 'form_add' in form.data:
                return self.create(data=form.cleaned_data)
            else:
                return self.update(data=form.cleaned_data)
        else:
            return JsonResponse({'msg':'error'})

           
        



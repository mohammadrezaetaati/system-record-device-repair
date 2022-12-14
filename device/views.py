


import json
from urllib import request


from persian import convert_en_numbers,convert_fa_numbers
from typing import Union,List

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView,UpdateView
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,JsonResponse
from django.db.models import QuerySet,ProtectedError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q,Max

from .forms import EditBrandCategoryForm, \
    OperationForm, AddDeviceForm,CategoryForm,\
        EditPartsForm,EditStatusForm,EditDeviceNgoingForm,\
            DeviceProvidestatus,DeviceUnrepairableForm,PrintWorkOrderForm
from .models import DeviceInput,Category,BrandCategory,Part,NumberPart
from place.models import Branch, Place
from user.permissions import RegistrarPermission,AdministratorPermission,StoreKeeperPermission
from .functions import create_work_order_number, g_to_p,save_date_time

import io
import os
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import reportlab




class PrintWorkOrder(View):

    # model = DeviceInput
    # template_name = 'device/print-work-order.html'
    # fields = ['work_order_number',]
    # success_url = '/device/add/'
    def get(self,request):
        return render(request,'device/print-work-order.html')
    # def form_invalid(self, form) -> HttpResponse:
    #     print(form.errors.get_json_data())
    #     return JsonResponse(form.errors.get_json_data())

    # def form_valid(self, form) -> HttpResponse:
    #     # print(self.get_object())
    #     print(form.data)
    #     buffer = io.BytesIO()
    #     p = canvas.Canvas(buffer)
    #     font='static/build/fonts/B_Yekan.ttf'
    #     pdfmetrics.registerFont(TTFont('B_Yekan.ttf', font))
    #     p.setFont('B_Yekan.ttf',20)
    #     p.drawString(300, 700,get_display(reshape('بسمه تعالی')))
    #     p.drawString(300, 200,get_display(reshape('چه خبر')))
    #     p.drawImage('static/images/god.png',100,500,width=100,height=50)
    #     p.showPage()
    #     p.save()
    #     buffer.seek(0)
    #     print('bbbbbbbbbbbbb')
    #     return FileResponse(buffer, as_attachment=True, filename='heloo.pdf')

        # return super().form_valid(form)
    def post(self, request):
        form=PrintWorkOrderForm(request.POST)
        if form.errors:
            return JsonResponse(form.errors.get_json_data())

        print(request.POST)
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        font='static/build/fonts/B_Yekan.ttf'
        pdfmetrics.registerFont(TTFont('B_Yekan.ttf', font))
        p.setFont('B_Yekan.ttf',20)
        p.drawString(300, 700,get_display(reshape('بسمه تعالی')))
        p.drawString(300, 200,get_display(reshape('چه خبر')))
        p.drawImage('static/images/god.png',100,500,width=100,height=50)
        p.showPage()
        p.save()
        buffer.seek(0)
        # return render(request,'device/device_all.html')
        # return redirect('/device/add/')
        # return HttpResponse('device/device_all.html')

        return FileResponse(buffer, as_attachment=True, filename='heloo.pdf')

        # return super().post(request, *args, **kwargs)
    # def post(self,request):
        
    #     buffer = io.BytesIO()
    #     p = canvas.Canvas(buffer)
    #     font='static/build/fonts/B_Yekan.ttf'
    #     pdfmetrics.registerFont(TTFont('B_Yekan.ttf', font))
    #     p.setFont('B_Yekan.ttf',20)
    #     p.drawString(300, 700,get_display(reshape('بسمه تعالی')))
    #     p.drawString(300, 200,get_display(reshape('چه خبر')))
    #     p.drawImage('static/images/god.png',100,500,width=100,height=50)
    #     p.showPage()
    #     p.save()
    #     buffer.seek(0)
    #     return FileResponse(buffer, as_attachment=True, filename='heloo.pdf')


def print_work_order(request):

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    font='static/build/fonts/B_Yekan.ttf'
    pdfmetrics.registerFont(TTFont('B_Yekan.ttf', font))
    p.setFont('B_Yekan.ttf',20)
    p.drawString(300, 700,get_display(reshape('بسمه تعالی')))
    p.drawString(300, 200,get_display(reshape('چه خبر')))
    p.drawImage('static/images/god.png',100,500,width=100,height=50)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='heloo.pdf')


user = get_user_model()

def home(request):
    return render(request,'device/index.html')
    
class SeeAllDevice(LoginRequiredMixin,RegistrarPermission,ListView):
    model = DeviceInput
    template_name = "device/device_all.html"
    context_object_name = "devices"

    def get_queryset(self):
        print(self.request.GET)
        return super().get_queryset()


class DeviceNgoing(LoginRequiredMixin,StoreKeeperPermission,View):
    device_id=None
    device=None

    def get(self,request):
        user=request.user
        if user.role == 'storekeeper':
            devices = DeviceInput.objects.filter(status='ngoing',place__storekeeper__username=user)
        else:
            devices=DeviceInput.objects.filter(status='ngoing')

        places=Place.objects.all()
        category=Category.objects.all()
        return render(request,'device/devices_ngoing.html',context={'devices':devices,'places':places,'category':category})

    def load_part_table_ajax(request):
        DeviceNgoing.device_id=request.GET.get('device_id')
        device=DeviceInput.objects.get(id=DeviceNgoing.device_id)
        print(device.category)
        parts=Part.objects.filter(category=device.category)
        return JsonResponse(list(parts.values('name','brand','id')),safe=False)
    
    def load_data_ajax(request):
        DeviceNgoing.device_id = request.GET.get("device_id")
        DeviceNgoing.device: DeviceInput = DeviceInput.objects.get(id=int(DeviceNgoing.device_id))
 
        # return JsonResponse(list(DeviceNgoing.device.values('branch','delivery','transferee_operator')),safe=False)
    
        return JsonResponse(
            {
                'device_id':DeviceNgoing.device_id,
                'phone':DeviceNgoing.device.branch.phone,
                'transferee_operator':DeviceNgoing.device.transferee_operator,
                "serial": DeviceNgoing.device.serial,
                'problem':DeviceNgoing.device.problem,
                'place':DeviceNgoing.device.place.name,
                'place_id':DeviceNgoing.device.place.id,
                'branch':DeviceNgoing.device.branch.name,
                "delivery": DeviceNgoing.device.delivery,
                'branch_id':DeviceNgoing.device.branch.id,
                'category':DeviceNgoing.device.category.name,
                'category_id':DeviceNgoing.device.category.id,
                'brand_category':DeviceNgoing.device.brand_category.name,
                'brand_category_id':DeviceNgoing.device.brand_category.id,   
            }
        )
    def obj_exists(self, data: str) -> bool:

        try:
            input=DeviceInput.objects.get(serial=convert_fa_numbers(data))
            if input.status != 'finished':
                return True
        except ObjectDoesNotExist:
            return False

    def update(self, data: dict) -> json:
        if DeviceNgoing.device.serial != data["serial"]:
            if self.obj_exists(data=data["serial"]):
                return JsonResponse({"msg": "exists"})
        DeviceInput.objects.filter(id=DeviceNgoing.device_id).update(serial=convert_fa_numbers(data.pop('serial')),**data)
        return JsonResponse({"msg": "success"})

    def ajax_delete(request):
        device_id = request.GET.get("device_id")
        input: DeviceInput = get_object_or_404(DeviceInput, id=int(device_id))
        input.delete()
        return JsonResponse({"msg": "success"})
    
    def ajax_repair_city(request):
        device_id = request.GET.get("device_id")
        DeviceInput.objects.filter(id=device_id).update(status='repair_city',repair_city_date=save_date_time()) 
        return JsonResponse({"msg": "success"})

    def post(self,request):
        if 'unrepairable' in request.POST:
            form=DeviceUnrepairableForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
                DeviceInput.objects.filter(id=DeviceNgoing.device_id).update(
                    status='unrepairable',
                    **form.cleaned_data,
                    exit_date=save_date_time(),
                    delivery_operator=f'{request.user.first_name} {request.user.last_name}'
                )
                return JsonResponse({"msg": "success"})
            else:
                return JsonResponse({"msg": "error"})

        if 'form_edit' in request.POST:
            form=EditDeviceNgoingForm(request.POST)
            print(form.errors,'jjjjjjjjjjjjjjj')
            if form.is_valid():
                return self.update(form.cleaned_data)
        input:DeviceInput=DeviceInput.objects.get(id=DeviceNgoing.device_id)
        part=None
        for data in request.POST:
            if len(request.POST.getlist(data))>1 :
                part='yes'
                print(request.POST.getlist(data))
                part_id=request.POST.getlist(data)[0]
                number=request.POST.getlist(data)[1]
                form=EditStatusForm({'number':number})
                if form.is_valid():
                    part=NumberPart.objects.get_or_create(number=form.cleaned_data['number'],part_id=int(part_id))
                    input.parts.add(part[0])
                    input.status='provide' 
                    input.provide_date=save_date_time()       

                else:
                    return JsonResponse({"msg": "error"})

        if request.POST['description'] != '':
            form=EditStatusForm({'description':request.POST['description']})
            print(form.errors,'ffffffffffffffffffffffffffffffffffffff')
            if form.is_valid():
                print('gggggggggggggggggggggggggg')
                input.description=form.cleaned_data['description']
                input.status='provide'
                input.provide_date=save_date_time()       
            else:
                return JsonResponse({"msg": "error"})
        elif part == None:
            return JsonResponse({'msg':'not device and description'})

        if 'finish_bool' in request.POST:
            form=EditStatusForm({'delivery':request.POST['delivery']})
            if form.is_valid():
                if form.cleaned_data['delivery'] == '' :
                    return JsonResponse({"msg": "null"})
                input.delivery_operator=f'{request.user.first_name} {request.user.last_name}'
                input.transferee=form.cleaned_data['delivery']
                input.status='finished'
                input.exit_date=save_date_time()
            else:
                return JsonResponse({"msg": "error"})
        if 'seal_bool' in request.POST:
            form=EditStatusForm({'seal_number':request.POST['seal_number']})
            if form.is_valid():
                if form.cleaned_data['seal_number'] == '' :
                    return JsonResponse({"msg": "null_seal"})
                input.seal_number=form.cleaned_data.get('seal_number')
            else:
                return JsonResponse({"msg": "error"})
        input.save()
        return JsonResponse({"msg": "success"})

class DeviceRepairCity(DeviceNgoing):
    
    def get(self,request):
        user=request.user
        if user.role == 'storekeeper':
            devices = DeviceInput.objects.filter(status='repair_city',place__storekeeper__username=user)
        else:
            devices=DeviceInput.objects.filter(status='repair_city')
        places=Place.objects.all()
        category=Category.objects.all()
        context={
            'devices':devices,
            'places':places,
            'category':category
        }
        return render(request,'device/repair_city.html',context=context)


class DeviceUnrepairable(DeviceNgoing):
    
    def get(self,request):
        user=request.user
        if user.role == 'storekeeper':
            devices = DeviceInput.objects.filter(status='unrepairable',place__storekeeper__username=user)
        else:
            devices=DeviceInput.objects.filter(status='unrepairable')
        places=Place.objects.all()
        category=Category.objects.all()
        context={
            'devices':devices,
            'places':places,
            'category':category
        }
        return render(request,'device/device_unrepairable.html',context=context)

class DeviceProvide(LoginRequiredMixin,StoreKeeperPermission,View):
    device_id=None
    def get(self,request):
        user=request.user
        if user.role == 'storekeeper':
            devices = DeviceInput.objects.filter(status='provide',place__storekeeper__username=user)
        else:
            devices=DeviceInput.objects.filter(status='provide')
        places=Place.objects.all()
        category=Category.objects.all()
        context={
            'devices':devices,
            'places':places,
            'category':category
        }
        return render(request,'device/device_provide.html',context=context)
    
    def get_device_id(request):
        DeviceProvide.device_id=request.GET.get('device_id')
        print(DeviceProvide.device_id)
        return JsonResponse({"msg": "success"})

    def return_status_ngoing(request):
        device_id=request.GET.get('device_id')
        input:DeviceInput=DeviceInput.objects.get(id=device_id)
        input.parts.clear()
        input.description= '-'
        input.exit_date='-'
        input.provide_date='-'
        input.status='ngoing'
        input.save()
        return JsonResponse({"msg": "success"})
        
    def edit_status_provide(self,data:dict,user):
        DeviceInput.objects.filter(id=DeviceProvide.device_id)\
            .update(
                transferee=data.get('delivery'),
                delivery_operator=user,
                status='finished',exit_date=save_date_time()
            )
        return JsonResponse({"msg": "success"})
      
    def post(self,request):
        print(request.POST)

        if 'status' in request.POST:
            form=DeviceProvidestatus(request.POST)
            print(form.errors)
            if form.is_valid():
                print(form.cleaned_data,'lllllllllllll')
                return self.edit_status_provide(data=form.cleaned_data,user=f'{request.user.first_name} {request.user.last_name}')
        


class DevicePrint(LoginRequiredMixin,RegistrarPermission,View):

    def get(self,request):
        devices=DeviceInput.objects.all()
        return render(request,'device/device_print.html',context={'devices':devices})


# class Operation(LoginRequiredMixin,RegistrarPermission,View):
#     """check operation for save or change status device"""
#     def get(self, request):

#         form = OperationForm()
#         context = {"form": form}
#         return render(request, "device/form_operation.html", context=context)
        
#     def device_exists(self,serial:str) -> bool:
#         device: Input = Input.objects.filter(
#                 serial=serial
#             ).exists()
#         return device

#     def status(self,serial) -> str:
#         """return status device"""
#         if self.device_exists(serial):
#             status=Input.objects.filter(serial=serial).values('status').last()
#             return status.get('status')
#     # def show_next_page(self,operation,serial):
#     #     if operation == 'Save' and  self.status(serial) == "دردست اقدام" :
#     #         return render(self.request, "form_operation.html", context={'status':True})
#     #     elif operation == 'Change_status' and self.status(serial="آماده به تحویل"):
#     #         return rend
#     def post(self, request):
#         form = OperationForm(request.POST)
#         if form.is_valid():
#             serial = form.cleaned_data.get("serial")
#             serial =convert_fa_numbers(serial)
#             print(self.status(serial))
#             if self.status(serial) == None or self.status(serial) == 'finished':
#                 request.session["serial"] = serial
#                 return redirect("/device/add/")
#             return render(request, "device/form_operation.html", context={'status':self.status(serial)})
#         return render(request, "device/form_operation.html")


class EditStatus(View):

    def get(self,request):
        parts=Part.objects.all()
        return render(request,'device/form_editstatus.html',context={'parts':parts})
    
    def post(self,request):
        form=EditStatusForm({'m':'2'})
        k={'m':[1,2,3],'b':[1,2]}
        for data in request.POST:
            if len(request.POST.getlist(data))>1 :
                print(request.POST.getlist(data))
                part_id=request.POST.getlist(data)[0]
                number=request.POST.getlist(data)[1]
                form=EditStatusForm({'number':number})
                if form.is_valid():
                    part=NumberPart.objects.get_or_create(number=form.cleaned_data['number'],part_id=int(part_id))
                    # print(part[0].id)
                    input:DeviceInput=DeviceInput.objects.filter(work_order_number='14016/2').values_list('parts')
                    # input.parts.add(part[0])
                    print(input)
                    print(form.cleaned_data)


class Storing(LoginRequiredMixin,StoreKeeperPermission,View):

    def get(self, request):
        devices=Category.objects.all()
        places=Place.objects.filter(storekeeper=request.user)
        count_place=places.count()
        if count_place == 1:
            branchs=Branch.objects.filter(place__storekeeper=request.user)
        else:
            branchs=None
        form=AddDeviceForm(request.GET)
        context = {
            'devices':devices,
            'places':places,
            'form':form,
            'count_place':count_place,
            'branchs':branchs
        }
        return render(request, "device/form_add_device.html", context=context)

    def device_exists(self,serial:str) -> bool:
        device: DeviceInput = DeviceInput.objects.filter(
                serial=serial
            ).exists()
        return device
    
    def status(self,serial) -> str:
        """return status device"""
        if self.device_exists(serial):
            status=DeviceInput.objects.filter(serial=serial).values('status').last()
            return status.get('status')

    def post(self, request):
        form = AddDeviceForm(request.POST)
        if form.errors:
            return JsonResponse(form.errors.get_json_data())
            # return HttpResponse(form.errors.get_json_data())
        if form.is_valid():
            serial=convert_fa_numbers(form.cleaned_data.pop('serial')) 
            if self.status(serial) == None or self.status(serial) == 'finished' or self.status(serial) == 'cancel':
                DeviceInput.objects.create(
                **form.cleaned_data,
                    # place=request.user.place,
                    # work_order_number=self.check_create_work_order_number(),
                    serial=serial,
                    # transferee_operator=f'{request.user.first_name} {request.user.last_name}',
                    request_date=save_date_time(),
                    status='waiting'
                )
                return JsonResponse({'msg':'success'})
            else:
                return JsonResponse({'msg':'error','status':self.status(serial)})
        return JsonResponse({'msg':'Notvalid'})

def check_create_work_order_number() -> str:
    """check filed work_order_number not null for create work_order_number"""
    try:
        last_object: DeviceInput = DeviceInput.objects.filter(~Q(work_order_number='',)).first()
        print(last_object.work_order_number,'lastttttttttttt')
        last_work_orde_number = last_object.work_order_number
    except AttributeError:
        last_work_orde_number = None
    work_order_number = create_work_order_number(last_work_orde_number)
    return work_order_number


class DeviceNew(LoginRequiredMixin,RegistrarPermission,View):

    def get(self,request):
        devices=DeviceInput.objects.filter(status='waiting').order_by('-request_date')
        # print(self.request.user.role)
        return render(request,'device/device_new.html',context={'devices':devices})

    def save(request):
        device_id=request.GET.get('device_id')
        print('gggggggggggg')
        DeviceInput.objects.filter(id=device_id).update(
            work_order_number=check_create_work_order_number(),
            transferee_operator=f'{request.user.first_name} {request.user.last_name}',
            entry_date=save_date_time(),
            status='ngoing'
        )
        return JsonResponse({'msg':'success'})

    def cancel(request):
        device_id=request.GET.get('device_id')


class DeviceWaiting(LoginRequiredMixin,StoreKeeperPermission,View):

    def get(self,request):
        devices=DeviceInput.objects.filter(status='waiting',place__storekeeper__username=request.user).order_by('-request_date')
        return render(request,'device/user/waiting.html',context={'devices':devices})

    def cancel(request):
        device_id=request.GET.get('device_id')
        DeviceInput.objects.get(id=device_id).delete()
        return JsonResponse({'msg':'success'})

class EditCategory(LoginRequiredMixin,RegistrarPermission,View):
    
    def get(self,request):
        context={'category':Category.objects.all()}
        return render(request,'device/form_add_category.html',context=context)

    def obj_exists(self,name:str,queryset:QuerySet) -> bool:
        return queryset.objects.filter(name=name).exists()

    def response(self,message:str) -> json:
        if message == 'success':
            return JsonResponse({'msg':'success'})
        elif message == 'exists':
            return JsonResponse({'msg':'exists'})
        elif message == 'protectederror':
            return JsonResponse({'msg':'protectederror'})
        elif message == 'ObjectDoesNotExist':
            return JsonResponse({'msg':'ObjectDoesNotExist'})
        else:
            return JsonResponse({'msg':'error'})

    def create(self,name:str,queryset:QuerySet) -> json:
        if self.obj_exists(name,queryset):
            return self.response('exists')
        queryset.objects.create(name=name)    
        return self.response('success')
        
    def update(self,queryset:Union[QuerySet,list[Category,BrandCategory]],name_new:str):
        if self.obj_exists(name_new,Category):
            return self.response('exists')
        queryset.update(name=name_new)
        return self.response('success')
    def delete(self,queryset:Union[QuerySet,list[Category,BrandCategory]]):
        if queryset:
            try:
                queryset.delete()
                return self.response('success')
            except ProtectedError:
                return self.response('protectederror')
        return self.response('error')
    def post(self,request):
        form=CategoryForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print(form.cleaned_data)
            if 'add' in request.POST:
                return self.create(name=convert_fa_numbers(form.cleaned_data.get('create_name')),queryset=Category)
            if 'edit' in request.POST:
                return self.update(queryset= form.cleaned_data.get('category'),name_new= convert_fa_numbers(form.cleaned_data.get('update_name')))
            if 'delete' in request.POST:
                print(form.cleaned_data.get('category'))
                return self.delete(form.cleaned_data.get('category'))
        else:
            return self.response('error')

       


class EditBrandCategory(EditCategory):

    def get(self,request):
        context={'category':Category.objects.all()}
        return render(request,'device/form_edit_brandcategory.html',context=context)

    def obj_exists(self,category:object,name:str) -> bool:
        return BrandCategory.objects.filter(category__name=category,name=name).exists()

    def create(self,category,name):
        category=Category.objects.get(name=category)
        if self.obj_exists(category,name):
            return self.response('exists')
        BrandCategory.objects.create(category=category,name=name)
        return self.response('success')

    def update(self, data:dict):
        if self.obj_exists(category=data.get('hidden'),name=convert_fa_numbers(data.get('update_name'))):
            return self.response('exists')
        data.get('brandcategory').update(name=convert_fa_numbers(data.get('update_name')))
        return self.response('success')

    def post(self,request):
            form=EditBrandCategoryForm(request.POST)
            if form.is_valid():
                try:
                    if 'add' in form.data:
                        return self.create(form.cleaned_data.get('hidden'),convert_fa_numbers(form.cleaned_data.get('create_name')))
                    if 'edit' in form.data:
                        return self.update(form.cleaned_data)
                    if 'delete' in form.data: 
                        return self.delete(form.cleaned_data.get('brandcategory'))
                except ObjectDoesNotExist:
                    return self.response('ObjectDoesNotExist')
            else:
                return self.response('error')


class Ajax:
    """
    It refreshes the input page without 
    reloading to load branch, brand_category
    """
        
    def load_Branchs(request):
        place_name = request.GET.get('place_name')
        print(place_name,'kkkkkkkkkkkkkkkkkkkk')
        branchs = Branch.objects.filter(place_id=place_name)
        print(branchs.values('id', 'name'))
        return JsonResponse(list(branchs.values('id', 'name')), safe=False)

    def load_brand_category(request):
        category_name=request.GET.get('category_name')
        brands=BrandCategory.objects.filter(category__name=category_name)
        return JsonResponse(list(brands.values('id','name')),safe=False)


class EditParts(LoginRequiredMixin,RegistrarPermission,View):
    part_id=None
    part=None
    
    def get(self,request):
        category=Category.objects.all()
        parts=Part.objects.all()
        print(parts)
        context={
            'category':category,
            'parts':parts
        }
        return render(request,'device/form_parts.html',context=context)

    def obj_exists(self,data:dict) -> bool:
        return Part.objects.filter(**data).exists()

    def create(self,data:dict) -> json:
        if self.obj_exists(data):
            return JsonResponse({'msg':'exists'})
        Part.objects.create(brand=convert_fa_numbers(data.pop('brand')),**data)
        return JsonResponse({'msg':'success'})
    
    def load_data_ajax(request) -> json:
        EditParts.part_id=request.GET.get('part_id')
        EditParts.part:Part=get_object_or_404(Part,id=int(EditParts.part_id))
        return JsonResponse({
                'name':EditParts.part.name,
                'brand':EditParts.part.brand,
            })
    
    def update(self,data:dict) -> json:
        category=data['category']
        if EditParts.part.name != data['name'] or \
            EditParts.part.brand != data['brand'] or \
                EditParts.part.category.name != category.name:
                if self.obj_exists(data):
                    return JsonResponse({'msg':'exists'})
        Part.objects.filter(id=int(EditParts.part_id))\
            .update(brand=convert_fa_numbers(data.pop('brand')),**data)
        return JsonResponse({'msg':'success'}) 

    def ajax_delete(request) -> json:
        part_id = request.GET.get("part_id")
        part: Part = get_object_or_404(Part, id=int(part_id))
        try:
            part.delete()
        except ProtectedError:
            return JsonResponse({"msg": "protectederror"})
        return JsonResponse({"msg": "success"})

    def post(self,request):
        print(request.POST,'postttttttttttttt')
        form=EditPartsForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.cleaned_data.update(
                {
                    'name':convert_fa_numbers(form.cleaned_data.get('name')),
                    'brand':convert_fa_numbers(form.cleaned_data.get('brand'))
                }
            )
            print(form.cleaned_data)
            if 'form_add' in form.data:
                return self.create(form.cleaned_data)
            else:
                return self.update(form.cleaned_data)
        else:
            return JsonResponse({"msg": "error"})






class Chart(View):

    def get(self,request):
        return render(request,'device/chart.html')
    
    

import persian

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from .forms import CheckSerialForm, AddDeviceForm, EditStatusLaptopForm
from .models import Device

from .functions import create_work_order_number


user = get_user_model()


class SeeAllDevice(ListView):
    model = Device
    template_name = "view_all_device.html"
    context_object_name = "devices"
    paginate_by: int = 5

    def get_ordering(self):
        return "-id"


class CheckSerial(View):
    """
    To register the tool, it first checks its status.
    According to the status, it directs the user to
    the desired page to continue the storage process.
    """

    def get(self, request):
        form = CheckSerialForm()
        context = {"form": form}
        return render(request, "form_checkserial.html", context=context)

    def post(self, request):
        form = CheckSerialForm(request.POST)
        if form.is_valid():
            serial = form.cleaned_data.get("serial")
            operation = form.cleaned_data.get("operation")
            persian_number = persian.convert_en_numbers(serial)
            request.session["serial"] = persian_number
            if operation == "Save":
                return redirect("/add-device/")
            else:
                return render(request, "form_editstatus.html")
        return render(request, "form_checkserial.html")


class EditStatus(CreateView):
    model = Device
    form_class = EditStatusLaptopForm
    template_name = "form_editstatus.html"
    success_url = "/edit-status"


class AddDevice(View):
    def get(self, request):
        try:
            device: Device = Device.objects.filter(
                serial=request.session.get("serial")
            ).last()
            status = device.status
        except ObjectDoesNotExist:
            device = None
        except AttributeError:
            status = None
        context = {"device": device, "status": status}
        if status and status == "دردست اقدام":
            return render(request, "form_checkserial.html", context=context)
        return render(request, "form_add_device.html", context=context)

    def post(self, request):
        """
        To create a work order number,
        first it is checked whether there is a number,
        then using the create_work_order_number function,
        the number is created and the new device is registered.
        """
        form = AddDeviceForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            try:
                last_object: Device = Device.objects.last()
                last_work_orde_number = last_object.work_order_number
            except AttributeError:
                last_work_orde_number = None
            work_order_number = create_work_order_number(last_work_orde_number)
            admin = user.objects.get(username="admin")
            Device.objects.create(
                **form.cleaned_data,
                work_order_number=work_order_number,
                serial=request.session.get("serial"),
                transferee=admin
            )
            return redirect("/check-serial/")
        return render(request, "form_add_device.html", context=context)

from django import forms


class CheckSerialForm(forms.Form):

    STATUS_CHOICES = [
        ("Save", "save"),
        ("Change_status", "change_status"),
    ]

    serial = forms.CharField(max_length=255)
    operation = forms.ChoiceField(widget=forms.Select, choices=STATUS_CHOICES)


class AddDeviceForm(forms.Form):

    STATUS_CHOICES = [
        ("کیس", "کیس"),
        ("پرینتر", "پرینتر"),
        ("لپتاب", "لپتاب"),
        ("تلویزیون", "تلویزیون"),
        ("مانیتور", "مانیتور"),
        ("تلفن", "تلفن"),
        ("محافظ برق", "محافظ برق"),
        ("دوربین", "دوربین"),
        ("بی سیم", "بی سیم"),
        ("متفرقه", "متفرقه"),
    ]

    category = forms.ChoiceField(widget=forms.Select, choices=STATUS_CHOICES)
    brand = forms.CharField(max_length=255)
    place = forms.CharField(max_length=255)
    branch = forms.CharField(max_length=255)
    delivery = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=255)
    problem = forms.CharField(max_length=255)


class EditStatusForm(forms.Form):
    description = forms.CharField(max_length=255)


class EditStatusLaptopForm(EditStatusForm):
    ram = forms.BooleanField()
    number_ram = forms.IntegerField()
    brand_ram = forms.CharField(max_length=255)
    cpu = forms.BooleanField()
    number_cpu = forms.IntegerField()
    brand_cpu = forms.CharField(max_length=255)
    gpu = forms.BooleanField()
    number_gpu = forms.IntegerField()
    brand_gpu = forms.CharField(max_length=255)
    mainboard = forms.BooleanField()
    hdd = forms.BooleanField()
    number_hdd = forms.IntegerField()
    brand_hdd = forms.CharField(max_length=255)
    ssd = forms.BooleanField()
    number_ssd = forms.IntegerField()
    brand_ssd = forms.CharField(max_length=255)

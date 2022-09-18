from django import forms

from .models import Place,Branch




class PlaceForm(forms.ModelForm):

    class Meta:
        model=Place
        fields='__all__'


class Branchform(forms.ModelForm):

    place=forms.ModelChoiceField(queryset=Place.objects.all(),to_field_name='id')

    class Meta:
        model=Branch
        fields='__all__'

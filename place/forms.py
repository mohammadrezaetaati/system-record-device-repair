from dataclasses import fields
from pyexpat import model
from django import forms

from .models import Place




class PlaceForm(forms.ModelForm):

    class Meta:
        model=Place
        fields='__all__'
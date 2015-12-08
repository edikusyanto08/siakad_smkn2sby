from django import forms
from .models import *

class MapelForm(forms.ModelForm):
    class Meta:
        model = Mapel
        widgets ={
            'nama_mapel': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'kode': forms.TextInput(attrs={'class': 'form-control'}),
            'type_mapel': forms.Select(attrs={'class': 'form-control'}),
            'pengajar': forms.SelectMultiple(attrs={'class': 'form-control chzn-select', 'data-placeholder': 'Pilih Guru...',}),
            'jurusan': forms.Select(attrs={'class': 'form-control chzn-select'}),
        }

class KompetensiKejuruanForm(forms.ModelForm):
    class Meta:
        model = KompetensiKejuruan
        widgets ={
            'mapel_induk': forms.Select(attrs={'class': 'form-control chzn-select', 'autofocus': 'autofocus'}),
            'nama_kompetensi': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MapelUNForm(forms.ModelForm):
    class Meta:
        model = MapelUN
        widgets ={
            'mapel': forms.Select(attrs={'class': 'form-control chzn-select', 'autofocus': 'autofocus'}),
        }
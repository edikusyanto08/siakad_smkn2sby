from django import forms
from .models import *

class JabatanForm(forms.ModelForm):
    class Meta:
        model = Jabatan
        widgets = {
            'nama_jabatan': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
        }

class PangkatForm(forms.ModelForm):
    class Meta:
        model = Pangkat
        widgets = {
            'nama_pangkat': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
        }

class ThnAjaranForm(forms.ModelForm):
    class Meta:
        model = ThnAjaran
        widgets = {
            'tahun_ajaran': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
        }


class JurusanForm(forms.ModelForm):
    class Meta:
        model = Jurusan
        widgets ={
            'nama_jurusan': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
        }

class RuangForm(forms.ModelForm):
    class Meta:
        model = Ruang
        widgets ={
            'nama_ruang': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
        }

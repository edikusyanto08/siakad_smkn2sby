from django import forms
from .models import *
from django.contrib import messages

class AbsensiSiswaForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(AbsensiSiswaForm,self).clean()
        siswanya = self.cleaned_data.get('siswa')
        kelasnya = self.cleaned_data.get('kelas')
        try:
            cek = Kelas.objects.get(siswa=siswanya)
        except:
            return cleaned_data
        if cek !=kelasnya:
            raise forms.ValidationError("Kelas siswa tidak cocok, terdaftar pada kelas %s" %(cek))
        return cleaned_data

    class Meta:
        model = AbsensiSiswa
        widgets ={
            'siswa': forms.Select(attrs={'class': 'form-control chzn-select', 'autofocus': 'autofocus'}),
            'kelas': forms.Select(attrs={'class': 'form-control chzn-select'}),
            'tanggal': forms.TextInput(attrs={'class': 'form-control', 'id':'dp1'}),
            'status': forms.Select(attrs={'class': 'form-control',}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control','id':'autosize2', 'rows':'3'}),
        }

class AbsensiGuruForm(forms.ModelForm):
    class Meta:
        model = AbsensiGuru
        widgets ={
            'guru': forms.Select(attrs={'class': 'form-control chzn-select', 'autofocus': 'autofocus'}),
            'jam_ke': forms.Select(attrs={'class': 'form-control chzn-select'}),
            'tanggal': forms.TextInput(attrs={'class': 'form-control', 'id':'dp1'}),
            'status': forms.Select(attrs={'class': 'form-control',}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control','id':'autosize2', 'rows':'3'}),
        }


from django import forms
from .models import *

class SiswaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SiswaForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['NIS'].widget.attrs['readonly'] = True

    def clean_NIS(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.NIS
        else:
            return self.cleaned_data['NIS']

    class Meta:
        model = Siswa
        exclude = ('user_login','hak_akses',)
        widgets = {
            'NIS': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'NISN': forms.TextInput(attrs={'class': 'form-control'}),
            'no_ijazah': forms.TextInput(attrs={'class': 'form-control'}),
            'nilai_un': forms.NumberInput(attrs={'class': 'form-control'}),
            'no_skhun': forms.TextInput(attrs={'class': 'form-control'}),
            'nama_lengkap' : forms.TextInput(attrs={'class': 'form-control'}),
            'sekolah_asal': forms.TextInput(attrs={'class': 'form-control'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-control'}),
            'tempat_lahir': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_lahir': forms.TextInput(attrs={'class': 'form-control', 'id':'dp1'}),
            'agama': forms.Select(attrs={'class': 'form-control'}),
            'tinggi': forms.NumberInput(attrs={'class': 'form-control'}),
            'berat': forms.NumberInput(attrs={'class': 'form-control'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control','id':'autosize1', 'rows':'3'}),
            'no_telpon': forms.TextInput(attrs={'class': 'form-control'}),
            'tinggal_dengan': forms.TextInput(attrs={'class': 'form-control'}),
            'jumlah_saudara': forms.NumberInput(attrs={'class': 'form-control'}),
            'jurusan': forms.Select(attrs={'class': 'form-control'}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control','id':'autosize2', 'rows':'3'}),
            'tanggal_masuk': forms.TextInput(attrs={'class': 'form-control', 'id':'dp2'}),
            'tanggal_lulus': forms.TextInput(attrs={'class': 'form-control', 'id':'dp3'}),
        }

class OrtuForm(forms.ModelForm):
    class Meta:
        model = Ortu
        fields = ('nama_ayah',
                  'nama_ibu',
                  'alamat_ortu',
                  'no_telpon',
                  'pendidikan_ayah',
                  'pekerjaan_ayah',
                  'penghasilan_ayah',
                  'pendidikan_ibu',
                  'pekerjaan_ibu',
                  'penghasilan_ibu',)
        widgets = {
            'nama_ayah': forms.TextInput(attrs={'class': 'form-control'}),
            'nama_ibu': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat_ortu': forms.Textarea(attrs={'class': 'form-control','id':'autosize3', 'rows':'3'}),
            'no_telpon': forms.TextInput(attrs={'class': 'form-control'}),
            'pendidikan_ayah': forms.Select(attrs={'class': 'form-control chosen-select'}),
            'pekerjaan_ayah': forms.TextInput(attrs={'class': 'form-control'}),
            'penghasilan_ayah': forms.NumberInput(attrs={'class': 'form-control'}),
            'pendidikan_ibu': forms.Select(attrs={'class': 'form-control chosen-select'}),
            'pekerjaan_ibu': forms.TextInput(attrs={'class': 'form-control'}),
            'penghasilan_ibu': forms.NumberInput(attrs={'class': 'form-control'}),
        }

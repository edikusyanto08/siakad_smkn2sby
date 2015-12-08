from django import forms
from .models import *

class GuruForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GuruForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['NIP'].widget.attrs['readonly'] = True
    PILIH_AKSES = (('kepsek','Kepsek'),
                   ('waka','Waka'),
                   ('staf','Staf'),
                   ('guru','Guru'),
                   ('siswa','Siswa'),
    )
    def clean_NIP(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.NIP
        else:
            return self.cleaned_data['NIP']
    #hak_akses = forms.ChoiceField(choices=PILIH_AKSES, widget = forms.Select(attrs={'class': 'form-control', 'autofocus': 'autofocus'}))
    class Meta:
        model = Guru
        exclude = ('user_login',)
        widgets = {
            'NIP': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'nama_lengkap': forms.TextInput(attrs={'class': 'form-control'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-control'}),
            'tempat_lahir': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_lahir': forms.TextInput(attrs={'class': 'form-control', 'id':'dp1'}),
            'agama': forms.Select(attrs={'class': 'form-control'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control','id':'autosize1', 'rows':'3'}),
            'no_telpon': forms.TextInput(attrs={'class': 'form-control'}),
            'no_rekening': forms.TextInput(attrs={'class': 'form-control'}),
            'golongan': forms.TextInput(attrs={'class': 'form-control'}),
            'jabatan': forms.Select(attrs={'class': 'form-control'}),
            'pangkat': forms.Select(attrs={'class': 'form-control'}),
            'NRG': forms.TextInput(attrs={'class': 'form-control'}),
            'no_sertifikat': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_masuk': forms.TextInput(attrs={'class': 'form-control', 'id':'dp2'}),
            'hak_akses': forms.Select(attrs={'class': 'form-control'}),
        }

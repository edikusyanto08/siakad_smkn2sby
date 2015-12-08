from django import forms
from .models import *

class KelasForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(KelasForm,self).clean()
        return cleaned_data
    def clean_siswa(self):
        get_siswa = self.cleaned_data.get('siswa')
        kuota = self.cleaned_data.get('jumlah_kuota')
        jurusan = self.cleaned_data.get('jurusan')
        for siswanya in get_siswa:
            if siswanya.jurusan != jurusan:
                raise forms.ValidationError("%s.Jurusan siswa tidak cocok!" %(siswanya))
        if get_siswa.count() > kuota:
            raise forms.ValidationError("Jumlah siswa melebihi kuota yang ditentukan.")
        return get_siswa
    class Meta:
        model = Kelas
        widgets ={
            'nama_kelas': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'jurusan': forms.Select(attrs={'class': 'form-control chzn-select'}),
            'jumlah_kuota': forms.NumberInput(attrs={'class': 'form-control'}),
            'kuota_terisi': forms.NumberInput(attrs={'class': 'form-control'}),
            'wali_kelas': forms.Select(attrs={'class': 'form-control chzn-select'}),
            'siswa': forms.SelectMultiple(attrs={'class': 'form-control chzn-select', 'data-placeholder': 'Pilih beberapa siswa...',}),
            'tahun_ajaran': forms.Select(attrs={'class': 'form-control chzn-select',}),
        }
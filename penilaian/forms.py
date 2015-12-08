from django import forms
from .models import *

class PeriodeForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(PeriodeForm,self).clean()
        return cleaned_data
    class Meta:
        model = Periode
        fields = ("semester", "tahun_ajaran", "kkm",)
        widgets = {
            'semester': forms.Select(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'tahun_ajaran': forms.Select(attrs={'class': 'form-control'}),
            'kkm': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class EntryNilaiSikapForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(EntryNilaiSikapForm,self).clean()
        return cleaned_data
    class Meta:
        model = NilaiSikap
        fields = ("observasi", "penilaian_diri", "penilaian_sejawat", "jurnal", "deskriptif",)
        widgets = {
            'observasi': forms.NumberInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'penilaian_diri': forms.NumberInput(attrs={'class': 'form-control'}),
            'penilaian_sejawat': forms.NumberInput(attrs={'class': 'form-control'}),
            'jurnal': forms.NumberInput(attrs={'class': 'form-control'}),
            'deskriptif': forms.Textarea(attrs={'class': 'form-control','id':'autosize1', 'rows':'3'}),
        }

class EntryNilaiKeterampilanForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(EntryNilaiKeterampilanForm,self).clean()
        return cleaned_data
    class Meta:
        model = NilaiKeterampilan
        fields = ("praktik","project", "portofolio", "deskriptif",)
        widgets = {
            'praktik': forms.NumberInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'project': forms.NumberInput(attrs={'class': 'form-control'}),
            'portofolio': forms.NumberInput(attrs={'class': 'form-control'}),
            'deskriptif': forms.Textarea(attrs={'class': 'form-control','id':'autosize1', 'rows':'3'}),
        }

class EntryNilaiKognitifForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(EntryNilaiKognitifForm,self).clean()
        return cleaned_data
    class Meta:
        model = NilaiKognitif
        fields = ("tugas","uh", "uts", "uas", "deskriptif",)
        widgets = {
            'tugas': forms.NumberInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'uh': forms.NumberInput(attrs={'class': 'form-control'}),
            'uts': forms.NumberInput(attrs={'class': 'form-control'}),
            'uas': forms.NumberInput(attrs={'class': 'form-control'}),
            'deskriptif': forms.Textarea(attrs={'class': 'form-control','id':'autosize1', 'rows':'3'}),
        }

class EntryNilaiKompetensiForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(EntryNilaiKompetensiForm,self).clean()
        return cleaned_data
    class Meta:
        model = NilaiKompetensi
        fields = ("jumlah_jam", "nilai",)
        widgets = {
            'jumlah_jam': forms.NumberInput(attrs={'class': 'form-control'}),
            'nilai': forms.NumberInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
        }

class EntryNilaiUSForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(EntryNilaiUSForm,self).clean()
        return cleaned_data
    class Meta:
        model = NilaiUS
        fields = ("nilai",)
        widgets = {
            'nilai': forms.NumberInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
        }

class EntryNilaiUNForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(EntryNilaiUNForm,self).clean()
        return cleaned_data
    class Meta:
        model = NilaiUN
        fields = ("nilai",)
        widgets = {
            'nilai': forms.NumberInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
        }

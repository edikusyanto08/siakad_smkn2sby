from django import forms
from .models import *
from kepegawaian.models import Guru

class WaktuForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(WaktuForm,self).clean()
        jam_mulai = self.cleaned_data.get('dari_jam')
        jam_selesai = self.cleaned_data.get('sampai_jam')
        try:
            if jam_selesai < jam_mulai:
                 raise forms.ValidationError("Jam mulai  harus lebih besar dari jam selesai.")
        except:
            raise forms.ValidationError("Jam mulai  harus lebih besar dari jam selesai.")
        return cleaned_data
    class Meta:
        model = Waktu
        widgets = {
            'hari': forms.Select(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'jam_ke': forms.NumberInput(attrs={'class': 'form-control'}),
            'dari_jam': forms.TextInput(attrs={'class': 'timepicker-24 form-control'}),
            'sampai_jam': forms.TextInput(attrs={'class': 'timepicker-24 form-control'}),
        }

class JadwalForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(JadwalForm,self).clean()
        return cleaned_data

    def clean_mapel(self):
        tahunnya = self.cleaned_data.get('tahun_ajaran')
        mapelnya = self.cleaned_data.get('mapel')
        waktunya = self.cleaned_data.get('waktu')
        gurus = Guru.objects.filter(mapeldiampu_guru=mapelnya)
        cek_mapel = Jadwal.objects.filter(tahun_ajaran=tahunnya, waktu=waktunya, mapel=mapelnya)
        cek_guru = Jadwal.objects.filter(tahun_ajaran=tahunnya, waktu=waktunya, mapel__pengajar=gurus)
        if cek_mapel.exists():
            raise forms.ValidationError("%s bentrok dengan %s" %(mapelnya, cek_mapel))
        elif cek_guru.exists():
            raise forms.ValidationError("%s mengajar di %s" %(gurus, cek_guru))
        return mapelnya

    def clean_ruang(self):
        ruangnya = self.cleaned_data.get('ruang')
        tahunnya = self.cleaned_data.get('tahun_ajaran')
        waktunya = self.cleaned_data.get('waktu')
        cek_ruang = Jadwal.objects.filter(tahun_ajaran=tahunnya, waktu=waktunya, ruang=ruangnya)
        if cek_ruang.exists():
            raise forms.ValidationError("Ruang %s digunakan %s" %(ruangnya, cek_ruang))
        return ruangnya

    class Meta:
        model = Jadwal
        fields = ("kelas", "tahun_ajaran","waktu","mapel", "ruang")
        widgets = {
            'waktu': forms.HiddenInput(attrs={'class': 'form-control'}),
            'mapel': forms.Select(attrs={'class': 'form-control chzn-select'}),
            'kelas': forms.HiddenInput(attrs={'class': 'form-control'}),
            'tahun_ajaran': forms.HiddenInput(attrs={'class': 'form-control'}),
            'ruang': forms.Select(attrs={'class': 'form-control chzn-select'}),
        }

class KegiatanForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(KegiatanForm,self).clean()
        date_mulai = self.cleaned_data.get('tgl_mulai')
        date_selesai = self.cleaned_data.get('tgl_selesai')
        try:
            if date_selesai < date_mulai:
                raise forms.ValidationError("Tanggal selesai harus lebih besar dari tanggal mulai atau sama.")
        except:
            raise forms.ValidationError("Tanggal selesai harus lebih besar dari tanggal mulai atau sama.")
        return cleaned_data
    class Meta:
        model = Kegiatan
        widgets = {
                'nama_kegiatan': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
                'urgensi': forms.Select(attrs={'class': 'form-control'}),
                'tgl_mulai': forms.TextInput(attrs={'class': 'form-control', 'id':'dp1'}),
                'tgl_selesai': forms.TextInput(attrs={'class': 'form-control', 'id':'dp2'}),
                'keterangan': forms.Textarea(attrs={'class': 'form-control','id':'autosize3', 'rows':'3'}),
            }

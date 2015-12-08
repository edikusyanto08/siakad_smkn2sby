from django.db import models
from data_master.models import Jabatan, Pangkat
from django.contrib.auth.models import User

import os
# Create your models here.
class Guru(models.Model):
    def direktori_nama_foto(instance, filename):
        ext = filename.split('.')[-1]
        nama_foto = "%s.%s" %(instance.NIP,ext)
        return os.path.join('foto/guru/', nama_foto)
    JENIS_KELAMIN = (('L', 'Laki-laki'),('P', 'Perempuan'))
    PILIH_AGAMA = (('Islam','Islam'),
                   ('Katolik','Katolik'),
                   ('Kristen','Kristen'),
                   ('Hindu','Hindu'),
                   ('Budha','Budha'),
                   ('Konghuchu','Konghuchu'),
    )
    PILIH_AKSES = (('kepsek','Kepsek'),
                   ('waka','Waka'),
                   ('staf','Staf'),
                   ('guru','Guru'),
                   ('siswa','Siswa'),
    )
    NIP = models.CharField(max_length=30, unique=True)
    nama_lengkap = models.CharField(max_length=50, verbose_name="Nama Lengkap")
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN, verbose_name="Jenis Kelamin")
    tempat_lahir = models.CharField(max_length=20, verbose_name="Asal", blank=True)
    tanggal_lahir = models.DateField(verbose_name="Tanggal Lahir")
    agama = models.CharField(max_length=10, choices=PILIH_AGAMA)
    alamat = models.TextField(max_length=100, verbose_name="Alamat Lengkap", blank=True)
    no_telpon = models.CharField(max_length=15, verbose_name="No Telepon", blank=True)
    no_rekening = models.CharField(max_length=30, verbose_name="No Rekening Bank", blank=True)
    pangkat = models.ForeignKey(Pangkat, on_delete=models.SET_NULL, null=True, blank=True)
    jabatan = models.ForeignKey(Jabatan, on_delete=models.SET_NULL, null=True, blank=True)
    NRG = models.CharField(max_length=30, blank=True)
    no_sertifikat = models.CharField(max_length=30, blank=True, verbose_name="No Sertifikat Pendidik")
    foto = models.ImageField(blank=True, upload_to=direktori_nama_foto, help_text="Ukuran 250x200 pixel")
    tanggal_masuk = models.DateField(verbose_name="Tanggal Masuk")
    diperbarui = models.DateTimeField(auto_now=True)
    user_login= models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="guru_user")
    hak_akses = models.CharField(max_length=20, choices=PILIH_AKSES, verbose_name="Hak Akses")

    def save(self, *args, **kwargs):
        try:
            this= Guru.objects.get(id=self.id)
            if this.foto!=self.foto:
                this.foto.delete(save=False)
        except: pass

        for field_name in ['nama_lengkap', 'tempat_lahir',]:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.title())
        super(Guru, self).save(*args, **kwargs)

    def gender(self):
        if self.jenis_kelamin == "L":
            return "Laki-laki"
        else:
            return "Perempuan"

    def delete(self, *args, **kwargs):
        this = Guru.objects.get(id=self.id)
        this.foto.delete(save=False)
        super(Guru, self).delete(*args, **kwargs)

    def __str__(self):
        return '%s - %s' %(self.NIP, self.nama_lengkap)


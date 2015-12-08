from django.db import models
from data_master.models import Jurusan
from django.contrib.auth.models import User

import os
# Create your models here.
class Siswa(models.Model):
    def direktori_nama_foto(instance, filename):
        ext = filename.split('.')[-1]
        nama_foto = "%s.%s" %(instance.NIS,ext)
        return os.path.join('foto/siswa/', nama_foto)

    JENIS_KELAMIN = (('L', 'Laki-laki'),('P', 'Perempuan'))
    PILIH_AGAMA = (('Islam','Islam'),
                   ('Katolik','Katolik'),
                   ('Kristen','Kristen'),
                   ('Hindu','Hindu'),
                   ('Budha','Budha'),
                   ('Konghuchu','Konghuchu'),
    )
    NIS = models.CharField(max_length=30, unique=True)
    NISN = models.CharField(max_length=30, blank=True)
    no_ijazah = models.CharField(max_length=30, blank=True, verbose_name="No Ijazah")
    no_skhun = models.CharField(max_length=30, blank=True, verbose_name="No SKHUN")
    nilai_un = models.DecimalField(max_digits=4, default=0, decimal_places=2, verbose_name="Nilai UN")
    sekolah_asal = models.CharField(max_length=30, blank=True)
    jurusan = models.ForeignKey(Jurusan, on_delete=models.SET_NULL, null=True)
    nama_lengkap = models.CharField(max_length=100, verbose_name="Nama Lengkap")
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN, verbose_name="Jenis Kelamin")
    tempat_lahir = models.CharField(max_length=20, verbose_name="Asal")
    tanggal_lahir = models.DateField(verbose_name="Tanggal Lahir")
    agama = models.CharField(max_length=10, choices=PILIH_AGAMA)
    tinggi = models.PositiveIntegerField(default=0)
    berat = models.PositiveIntegerField(default=0)
    alamat = models.CharField(max_length=100, verbose_name="Alamat Lengkap", blank=True)
    no_telpon = models.CharField(max_length=15, blank=True, verbose_name="No Telepon")
    tinggal_dengan = models.CharField(max_length=30, verbose_name="Tinggal Dengan", blank=True)
    jumlah_saudara = models.PositiveIntegerField(default=0, verbose_name="Jumlah Saudara Kandung")
    foto = models.ImageField(blank=True, upload_to=direktori_nama_foto)
    keterangan = models.TextField(blank=True)
    tanggal_masuk = models.DateField(verbose_name="Tanggal Masuk")
    tanggal_lulus = models.DateField(verbose_name="Tanggal Lulus", blank=True, null=True)
    diperbarui = models.DateTimeField(auto_now=True)
    user_login= models.OneToOneField(User, null=True, blank=True,on_delete=models.SET_NULL, related_name="siswa_user")
    hak_akses = models.CharField(max_length=20, default="siswa", verbose_name="Hak Akses")

    def gender(self):
        if self.jenis_kelamin == "L":
            return "Laki-laki"
        else:
            return "Perempuan"

    def save(self, *args, **kwargs):
        try:
            this= Siswa.objects.get(id=self.id)
            if this.foto != self.foto:
                this.foto.delete(save=False)
        except: pass

        for field_name in ['nama_lengkap', 'tempat_lahir', 'tinggal_dengan']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.title())
        super(Siswa, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        this = Siswa.objects.get(id=self.id)
        this.foto.delete(save=False)
        super(Siswa, self).delete(*args, **kwargs)

    def __str__(self):
        return '%s - %s | %s' %(self.NIS, self.nama_lengkap, self.jurusan)

class Ortu(models.Model):
    PILIH_PENDIDIKAN = (('SD','SD / Sederajat'),
                        ('SMP','SMP / Sederajat'),
                        ('SMA','SMA / Sederajat'),
                        ('Diploma','Diploma'),
                        ('S1','Strata 1'),
                        ('S2','Strata 2'),
                        ('Lainnya','Lainnya'),
    )
    siswa = models.OneToOneField(Siswa, related_name="ortu_siswa")
    nama_ayah = models.CharField(max_length=100, verbose_name="Nama Ayah Kandung", blank=True)
    nama_ibu = models.CharField(max_length=100, verbose_name="Nama Ibu Kandung", blank=True)
    alamat_ortu = models.CharField(max_length=100, verbose_name="Alamat Lengkap", blank=True)
    no_telpon = models.CharField(max_length=15, verbose_name="Nomor kontak yang bisa dihubungi", blank=True)
    pendidikan_ayah = models.CharField(max_length=30, choices=PILIH_PENDIDIKAN, blank=True)
    pekerjaan_ayah = models.CharField(max_length=100, blank=True)
    penghasilan_ayah = models.PositiveIntegerField(default=0)
    pendidikan_ibu = models.CharField(max_length=30, choices=PILIH_PENDIDIKAN, blank=True)
    pekerjaan_ibu = models.CharField(max_length=100, blank=True)
    penghasilan_ibu = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):

        for field_name in ['nama_ayah', 'nama_ibu', 'pekerjaan_ayah', 'pekerjaan_ibu',]:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.title())
        super(Ortu, self).save(*args, **kwargs)


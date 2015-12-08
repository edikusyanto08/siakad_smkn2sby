from django.db import models
from kepegawaian.models import Guru
from data_master.models import Jurusan
# Create your models here.
class Mapel(models.Model):
    TYPE_MAPEL = (('Kelompok A','Kelompok A (Wajib)'),
                   ('Kelompok B','Kelompok B (Wajib)'),
                   ('Dasar Bidang ','Kelompok C (Dasar Bidang)'),
                  ('Dasar Program','Kelompok C (Dasar Program)'),
                  ('Mulok','Muatan Lokal'),
    )

    nama_mapel = models.CharField(max_length=50, verbose_name="Nama Mata Pelajaran")
    type_mapel = models.CharField(max_length=30, choices=TYPE_MAPEL, verbose_name="Kategori")
    jurusan = models.ForeignKey(Jurusan, verbose_name="Jurusan", blank=True, null=True)
    kode = models.CharField(max_length=10, verbose_name="Kode Mapel")
    pengajar = models.ManyToManyField(Guru, verbose_name="Pengajar", blank=True, null=True, through="MapelDiampu")

    def save(self, *args, **kwargs):
        for field_name in ['nama_mapel']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.title())
        super(Mapel, self).save(*args, **kwargs)
        for field_name in ['kode']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())
        super(Mapel, self).save(*args, **kwargs)

    def __str__(self):
        return '%s | %s' %(self.jurusan, self.nama_mapel)

class MapelDiampu(models.Model):
    mapel = models.ForeignKey(Mapel, related_name="mapeldiampu_mapel")
    pengajar = models.ForeignKey(Guru, related_name="mapeldiampu_guru")

    def __str__(self):
        return '%s - %s' %(self.mapel.nama_mapel, self.pengajar.nama_lengkap)

class KompetensiKejuruan(models.Model):
    mapel_induk = models.ForeignKey(Mapel)
    nama_kompetensi = models.CharField(max_length=255, verbose_name="Nama Kompetensi")

    def save(self, *args, **kwargs):
        for field_name in ['nama_kompetensi']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.title())
        super(KompetensiKejuruan, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' %(self.nama_kompetensi)

class MapelUN(models.Model):
    mapel = models.ForeignKey(Mapel, verbose_name="Mata Pelajaran", related_name="mapelun_mapel")

    def __str__(self):
        return '%s' %(self.mapel.nama_mapel)




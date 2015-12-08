from django.db import models
from kepegawaian.models import Guru
from kesiswaan.models import Siswa
from kelas.models import Kelas
from jadwal.models import Waktu
# Create your models here.

class AbsensiSiswa(models.Model):
    KET =(("Sakit", "Sakit"),
              ("Ijin", "Ijin"),
              ("Alpha", "Tanpa Keterangan"),
    )
    siswa = models.ForeignKey(Siswa)
    kelas = models.ForeignKey(Kelas)
    tanggal = models.DateField()
    status = models.CharField(max_length=20, choices=KET)
    keterangan = models.TextField(blank=True)
    tgl_entry = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s | %s' %(self.tanggal, self.siswa.nama_lengkap)

class AbsensiGuru(models.Model):
    KET =(("Sakit", "Sakit"),
              ("Ijin", "Ijin"),
              ("Alpha", "Tanpa Keterangan"),
    )
    guru = models.ForeignKey(Guru)
    tanggal = models.DateField()
    jam_ke = models.ForeignKey(Waktu, verbose_name="Pada jam ke", blank= True, null=True)
    status = models.CharField(max_length=20, choices=KET)
    keterangan = models.TextField(blank=True)
    tgl_entry = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s | %s' %(self.tanggal, self.guru.nama_lengkap)


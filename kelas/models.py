from django.db import models
from data_master.models import Jurusan, ThnAjaran
from kepegawaian.models import Guru
from kesiswaan.models import Siswa
# Create your models here.

class Kelas(models.Model):
    tahun_ajaran = models.ForeignKey(ThnAjaran, related_name="kelas_thnajaran", verbose_name="Tahun Ajaran")
    nama_kelas = models.CharField(max_length=30, verbose_name="Nama Kelas")
    jurusan = models.ForeignKey(Jurusan)
    jumlah_kuota = models.PositiveIntegerField(default=0)
    wali_kelas = models.ForeignKey(Guru, verbose_name="Wali Kelas", related_name="kelas_guru")
    siswa = models.ManyToManyField(Siswa, verbose_name="Pilih siswa", blank=True, null=True, through="Kelas_Siswa")

    def save(self, *args, **kwargs):
        for field_name in ['nama_kelas']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())
        super(Kelas, self).save(*args, **kwargs)

    def __str__(self):
        return '%s | %s' %(self.nama_kelas, self.wali_kelas.nama_lengkap)

class Kelas_Siswa(models.Model):
    kelas = models.ForeignKey(Kelas)
    tahun_ajaran = models.ForeignKey(ThnAjaran)
    siswa = models.ForeignKey(Siswa, related_name="kelas_siswa")

    class Meta:
        unique_together = ("siswa", "tahun_ajaran")

    def __str__(self):
        return '%s | %s' %(self.kelas, self.siswa.nama_lengkap)

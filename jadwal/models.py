from django.db import models
from data_master.models import ThnAjaran, Ruang
from kelas.models import Kelas
from mapel.models import MapelDiampu
# Create your models here.

class Waktu(models.Model):
    HARI = (('Senin', 'Senin'),
            ('Selasa', 'Selasa'),
            ('Rabu', 'Rabu'),
            ('Kamis', 'Kamis'),
            ('Jumat', 'Jumat'),
            ('Sabtu', 'Sabtu'),

    )
    hari = models.CharField(max_length=10, choices=HARI)
    jam_ke = models.PositiveIntegerField(default=1, verbose_name="Jam Ke")
    dari_jam = models.TimeField(verbose_name="Mulai Jam")
    sampai_jam = models.TimeField(verbose_name="Sampai Jam")

    def save(self, *args, **kwargs):
        for field_name in ['hari']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.title())
        super(Waktu, self).save(*args, **kwargs)

    def __str__(self):
        return '%s Jam ke - %s' %(self.hari, self.jam_ke)

class Jadwal(models.Model):
    waktu = models.ForeignKey(Waktu, related_name="jadwal_waktu")
    kelas = models.ForeignKey(Kelas, related_name="jadwal_kelas")
    ruang = models.ForeignKey(Ruang, related_name="jadwal_ruang", null=True, on_delete=models.SET_NULL )
    mapel = models.ForeignKey(MapelDiampu, related_name="jadwal_mapeldiampu", blank=True, null=True, on_delete=models.SET_NULL )
    tahun_ajaran = models.ForeignKey(ThnAjaran, related_name="jadwal_thn")

    def __str__(self):
        return '%s | %s' %(self.kelas.nama_kelas, self.mapel)

class Kegiatan(models.Model):
    URGENSI =(("khusus", "Khusus"),
              ("normal", "Normal"),
              ("perhatian", "Perhatian"),
              ("penting", "Penting"),
              ("sangat penting", "Sangat Penting"),

    )
    nama_kegiatan = models.CharField(max_length=100, verbose_name="Nama Kegiatan")
    urgensi = models.CharField(max_length=20, choices=URGENSI)
    tgl_mulai = models.DateField()
    tgl_selesai = models.DateField()
    keterangan = models.TextField(blank=True, null=True)

    def get_warna(self):
        if self.urgensi =="khusus":
            return "#b7b7b7"
        elif self.urgensi =="normal":
            return "#00cc33"
        elif self.urgensi =="perhatian":
            return "#0099ff"
        elif self.urgensi =="penting":
            return "#ff9900"
        else:
            return "#fa0a2e"

    def __str__(self):
        return '%s' %(self.nama_kegiatan)
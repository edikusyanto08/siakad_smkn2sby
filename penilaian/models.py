from django.db import models
from mapel.models import *
from kelas.models import Kelas
from kepegawaian.models import Guru
from kesiswaan.models import Siswa
from data_master.models import ThnAjaran
from django.core.validators import MaxValueValidator

# Create your models here.
class Periode(models.Model):
    SEMESTER = (('Genap','Genap'),
            ('Ganjil','Ganjil'),
    )
    semester = models.CharField(max_length=10, choices=SEMESTER)
    tahun_ajaran = models.ForeignKey(ThnAjaran, related_name="periode_tahun")
    kkm = models.DecimalField(max_digits=5, default=0, decimal_places=2)
    aktif = models.PositiveSmallIntegerField(default=0)
    verifikasi = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "%s %s" %(self.semester, self.tahun_ajaran)

class NilaiSikap(models.Model):
    siswa = models.ForeignKey(Siswa, related_name="sikap_siswa")
    kelas = models.ForeignKey(Kelas, related_name="sikap_kelas")
    mapel = models.ForeignKey(Mapel, related_name="sikap_mapel")
    periode = models.ForeignKey(Periode, related_name="sikap_periode")
    pengajar = models.ForeignKey(Guru, related_name="sikap_guru")
    observasi = models.DecimalField(default=0, max_digits=5,decimal_places=2, validators=[MaxValueValidator(100.00)])
    penilaian_diri = models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)])
    penilaian_sejawat =  models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)])
    jurnal =  models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)])
    rerata =  models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)], verbose_name="Rata-rata Nilai")
    konversi = models.DecimalField(default=1, max_digits=5, decimal_places=2, validators=[MaxValueValidator(4.00)])
    predikat = models.CharField(max_length=2, default="D")
    deskriptif = models.CharField(max_length=500, verbose_name="Nilai Deskriptif", blank=True)

class NilaiKeterampilan(models.Model):
    siswa = models.ForeignKey(Siswa, related_name="keterampilan_siswa")
    kelas = models.ForeignKey(Kelas, related_name="keterampilan_kelas")
    mapel = models.ForeignKey(Mapel, related_name="keterampilan_mapel")
    periode = models.ForeignKey(Periode, related_name="keterampilan_periode")
    pengajar = models.ForeignKey(Guru, related_name="keterampilan_guru")
    praktik = models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)])
    project = models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)])
    portofolio =  models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)])
    rerata =  models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)], verbose_name="Rata-rata Nilai")
    konversi = models.DecimalField(default=1, max_digits=5, decimal_places=2, validators=[MaxValueValidator(4.00)])
    predikat = models.CharField(max_length=2, default="D")
    deskriptif = models.CharField(max_length=500, verbose_name="Nilai Deskriptif", blank=True)

class NilaiKognitif(models.Model):
    siswa = models.ForeignKey(Siswa, related_name="kognitif_siswa")
    kelas = models.ForeignKey(Kelas, related_name="kognitif_kelas")
    mapel = models.ForeignKey(Mapel, related_name="kognitif_mapel")
    periode = models.ForeignKey(Periode, related_name="kognitif_periode")
    pengajar = models.ForeignKey(Guru, related_name="kognitif_guru")
    tugas = models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)])
    uh = models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)], verbose_name="Ulangan Harian")
    uts =  models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)], verbose_name="UTS")
    uas =  models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)], verbose_name="UAS")
    rerata =  models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)], verbose_name="Rata-rata Nilai")
    konversi = models.DecimalField(default=1, max_digits=5, decimal_places=2, validators=[MaxValueValidator(4.00)])
    predikat = models.CharField(max_length=2, default="D")
    deskriptif = models.CharField(max_length=500, verbose_name="Nilai Deskriptif", blank=True)

class NilaiTotal(models.Model):
    siswa = models.ForeignKey(Siswa, related_name="rapor_siswa")
    kelas = models.ForeignKey(Kelas, related_name="rapor_kelas")
    mapel = models.ForeignKey(Mapel, related_name="rapor_mapel")
    periode = models.ForeignKey(Periode, related_name="rapor_periode")
    pengajar = models.ForeignKey(Guru, related_name="rapor_guru")
    nilai_sikap = models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)])
    nilai_sikap_konv = models.DecimalField(default=1, max_digits=5, decimal_places=2, validators=[MaxValueValidator(4.00)])
    nilai_sikap_pre = models.CharField(max_length=2, default="D")
    nilai_keterampilan = models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)])
    nilai_keterampilan_konv = models.DecimalField(default=1, max_digits=5, decimal_places=2, validators=[MaxValueValidator(4.00)])
    nilai_keterampilan_pre = models.CharField(max_length=2, default="D")
    nilai_kognitif = models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)])
    nilai_kognitif_konv = models.DecimalField(default=1, max_digits=5, decimal_places=2, validators=[MaxValueValidator(4.00)])
    nilai_kognitif_pre = models.CharField(max_length=2, default="D")
    rerata =  models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)], verbose_name="Rata-rata Nilai")
    konversi = models.DecimalField(default=1, max_digits=5, decimal_places=2, validators=[MaxValueValidator(4.00)])
    predikat = models.CharField(max_length=2, default="D")
    keterangan = models.CharField(max_length=30, default="Belum Tuntas")

class NilaiUN(models.Model):
    siswa = models.ForeignKey(Siswa, related_name="nilaiun_siswa")
    kelas = models.ForeignKey(Kelas, related_name="nilaiun_kelas")
    mapel = models.ForeignKey(Mapel, related_name="nilaiun_mapel")
    tahun_ajaran = models.ForeignKey(ThnAjaran, related_name="nilaiun_thn")
    nilai = models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)])
    konversi = models.DecimalField(default=1, max_digits=5, decimal_places=2, validators=[MaxValueValidator(4.00)])
    predikat = models.CharField(max_length=2, default="D")

    def __str__(self):
        return "%s | %s  %s" %(self.tahun_ajaran, self.siswa.nama_lengkap, self.mapel)

class NilaiUS(models.Model):
    siswa = models.ForeignKey(Siswa, related_name="nilaius_siswa")
    kelas = models.ForeignKey(Kelas, related_name="nilaius_kelas")
    mapel = models.ForeignKey(Mapel, related_name="nilaius_mapel")
    tahun_ajaran = models.ForeignKey(ThnAjaran, related_name="nilaius_thn")
    nilai = models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)])
    konversi = models.DecimalField(default=1, max_digits=5, decimal_places=2, validators=[MaxValueValidator(4.00)])
    predikat = models.CharField(max_length=2, default="D")

    def __str__(self):
        return "%s | %s  %s" %(self.tahun_ajaran, self.siswa.nama_lengkap, self.mapel)

class NilaiKompetensi(models.Model):
    siswa = models.ForeignKey(Siswa, related_name="kompetensi_siswa")
    kelas = models.ForeignKey(Kelas, related_name="kompetensi_kelas")
    mapel = models.ForeignKey(Mapel, related_name="kompetensi_mapel")
    kompetensi = models.ForeignKey(KompetensiKejuruan, related_name="kompetensi_kompetensi")
    periode = models.ForeignKey(Periode, related_name="kompetensi_periode", null=True)
    pengajar = models.ForeignKey(Guru, related_name="kompetensi_guru", null=True)
    jumlah_jam = models.PositiveIntegerField(default=0, verbose_name="Jumlah Jam")
    nilai = models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)])
    konversi = models.DecimalField(default=1, max_digits=5, decimal_places=2, validators=[MaxValueValidator(4.00)])
    predikat = models.CharField(max_length=2, default="D")

    def __str__(self):
        return "%s %s | %s" %(self.periode, self.siswa.nama_lengkap, self.kompetensi.nama_kompetensi)
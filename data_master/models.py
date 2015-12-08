from django.db import models

# Create your models here.
class ThnAjaran(models.Model):
    tahun_ajaran = models.CharField(max_length=30, verbose_name="Tahun Ajaran")

    def __str__(self):
        return '%s' %(self.tahun_ajaran)

class Jurusan(models.Model):
    nama_jurusan = models.CharField(max_length=50, verbose_name="Nama Jurusan")

    def save(self, *args, **kwargs):
        for field_name in ['nama_jurusan']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.title())
        super(Jurusan, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' %(self.nama_jurusan)


class Jabatan(models.Model):
    nama_jabatan = models.CharField(max_length=50, verbose_name="Nama Jabatan")

    def save(self, *args, **kwargs):
        for field_name in ['nama_jabatan']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.title())
        super(Jabatan, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' %(self.nama_jabatan)

class Pangkat(models.Model):
    nama_pangkat = models.CharField(max_length=50, verbose_name="Nama Pangkat")

    def save(self, *args, **kwargs):
        for field_name in ['nama_pangkat']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.title())
        super(Pangkat, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' %(self.nama_pangkat)

class Ruang(models.Model):
    nama_ruang = models.CharField(max_length=50, verbose_name="Nama Ruang", unique=True)

    def save(self, *args, **kwargs):
        for field_name in ['Nama Ruang']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.title())
        super(Ruang, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' %(self.nama_ruang)




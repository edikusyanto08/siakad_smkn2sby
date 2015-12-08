from django.contrib import admin
from .models import *
# Register your models here.

class WaktuAdmin(admin.ModelAdmin):
    class Meta:
        model = Waktu

admin.site.register(Waktu, WaktuAdmin)

class JadwalAdmin(admin.ModelAdmin):
    class Meta:
        model = Jadwal

admin.site.register(Jadwal, JadwalAdmin)

class KegiatanAdmin(admin.ModelAdmin):
    class Meta:
        model = Kegiatan

admin.site.register(Kegiatan, KegiatanAdmin)
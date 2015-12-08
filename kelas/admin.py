from django.contrib import admin
from .models import *
# Register your models here.
class KelasAdmin(admin.ModelAdmin):
    class Meta:
        model = Kelas
admin.site.register(Kelas, KelasAdmin)

class Kelas_SiswaAdmin(admin.ModelAdmin):
    class Meta:
        model = Kelas_Siswa
admin.site.register(Kelas_Siswa, Kelas_SiswaAdmin)
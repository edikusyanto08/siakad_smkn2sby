from django.contrib import admin
from .models import *
# Register your models here.
class AbsensiSiswaAdmin(admin.ModelAdmin):
    class Meta:
        model = AbsensiSiswa
admin.site.register(AbsensiSiswa, AbsensiSiswaAdmin)

class AbsensiGuruAdmin(admin.ModelAdmin):
    class Meta:
        model = AbsensiGuru

admin.site.register(AbsensiGuru, AbsensiGuruAdmin)
from django.contrib import admin
from .models import *

class PeriodeAdmin(admin.ModelAdmin):
    class Meta:
        model = Periode

admin.site.register(Periode, PeriodeAdmin)

class NilaiSikapAdmin(admin.ModelAdmin):
    class Meta:
        model = NilaiSikap

admin.site.register(NilaiSikap, NilaiSikapAdmin)

class NilaiKeterampilanAdmin(admin.ModelAdmin):
    class Meta:
        model = NilaiKeterampilan

admin.site.register(NilaiKeterampilan, NilaiKeterampilanAdmin)

class NilaiKognitifAdmin(admin.ModelAdmin):
    class Meta:
        model = NilaiKognitif

admin.site.register(NilaiKognitif, NilaiKognitifAdmin)
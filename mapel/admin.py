from django.contrib import admin
from .models import *

# Register your models here.
class MapelAdmin(admin.ModelAdmin):
    class Meta:
        model = Mapel

admin.site.register(Mapel, MapelAdmin)

class KompetensiAdmin(admin.ModelAdmin):
    class Meta:
        model = KompetensiKejuruan

admin.site.register(KompetensiKejuruan, KompetensiAdmin)

class MapelDiampuAdmin(admin.ModelAdmin):
    class Meta:
        model = MapelDiampu

admin.site.register(MapelDiampu, MapelDiampuAdmin)
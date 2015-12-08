from django.contrib import admin
from .models import *

# Register your models here.
class SiswaAdmin(admin.ModelAdmin):
    class Meta:
        model = Siswa

admin.site.register(Siswa, SiswaAdmin)

class OrtuAdmin(admin.ModelAdmin):
    class Meta:
        model = Ortu

admin.site.register(Ortu, OrtuAdmin)
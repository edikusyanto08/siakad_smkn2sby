from django.contrib import admin
from .models import *
# Register your models here.

class JabatanAdmin(admin.ModelAdmin):
    class Meta:
        model = Jabatan

admin.site.register(Jabatan, JabatanAdmin)

class PangkatAdmin(admin.ModelAdmin):
    class Meta:
        model = Pangkat

admin.site.register(Pangkat, PangkatAdmin)

class ThnAjaranAdmin(admin.ModelAdmin):
    class Meta:
        model = ThnAjaran

admin.site.register(ThnAjaran, ThnAjaranAdmin)

class JurusanAdmin(admin.ModelAdmin):
    class Meta:
        model = Jurusan

admin.site.register(Jurusan, JabatanAdmin)

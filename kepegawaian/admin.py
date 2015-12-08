from django.contrib import admin
from .models import *

# Register your models here.
class GuruAdmin(admin.ModelAdmin):
    class Meta:
        model = Guru

admin.site.register(Guru, GuruAdmin)
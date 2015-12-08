from django.conf.urls import patterns, url
from absensi import views

urlpatterns = patterns('absensi',
    url(r'^$', views.absen_guru, name='absen_guru'),
    url(r'^tambah/$', views.tambah_abs_guru, name='tambah_abs_guru'),
    url(r'^hapus/(?P<idData>\d+)/$', views.hapus_abs_guru, name='hapus_abs_guru'),
)
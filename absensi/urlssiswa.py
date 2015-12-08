from django.conf.urls import patterns, url
from absensi import views

urlpatterns = patterns('absensi',
    url(r'^$', views.absen_siswa, name='absen_siswa'),
    url(r'^tambah/$', views.tambah_abs_siswa, name='tambah_abs_siswa'),
    url(r'^hapus/(?P<idData>\d+)/$', views.hapus_abs_siswa, name='hapus_abs_siswa'),
)
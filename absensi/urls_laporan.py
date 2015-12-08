from django.conf.urls import patterns, url, include
from absensi import views
urlpatterns = patterns('laporan',
    url(r'^$', views.laporan, name='laporan'),
    url(r'^absensi/$', views.laporan, name='laporan_absensi'),
    url(r'^absensi/siswa/$', views.absensi_siswa, name='absensi_siswa'),
    url(r'^absensi/siswa/cetak/$', views.cetak_absensi_siswa, name='cetak_absensi_siswa'),
    url(r'^absensi/guru/$', views.absensi_guru, name='absensi_guru'),
    url(r'^absensi/guru/cetak/$', views.cetak_absensi_guru, name='cetak_absensi_guru'),
    url(r'^transkrip/$', views.transkrip, name='transkrip'),
)
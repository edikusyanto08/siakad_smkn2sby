from django.conf.urls import patterns, url
from jadwal import views

urlpatterns = patterns('jadwal',
    url(r'^waktu/$', views.waktu, name='waktu'),
    url(r'^waktu/tambah/$', views.tambah_waktu, name='tambah_waktu'),
    url(r'^waktu/ubah/(?P<idWaktu>\d+)/$', views.ubah_waktu, name='ubah_waktu'),
    url(r'^waktu/hapus/(?P<idWaktu>\d+)/$', views.hapus_waktu, name='hapus_waktu'),
    url(r'^kelas/$', views.kelas, name='jadwal_kelas'),
    url(r'^kelas/(?P<idKelas>\d+)/$', views.jadwal, name='jadwal'),
    url(r'^kelas/all/(?P<idThn>\d+)/$', views.jadwal_all, name='jadwal_all'),
    #url(r'^kelas/(?P<idKelas>\d+)/tambah/$', views.tambah_jadwal, name='tambah_jadwal'),
    url(r'^kelas/(?P<idJadwal>\d+)/tambah/$', views.ubah_jadwal, name='ubah_jadwal'),
    url(r'^kelas/(?P<idJadwal>\d+)/hapus/$', views.hapus_jadwal, name='hapus_jadwal'),
    url(r'^jadwalku/$', views.myjadwal, name='myjadwal'),
    url(r'^jadwalku/cetak/$', views.cetak_myjadwal, name='cetak_myjadwal'),
)
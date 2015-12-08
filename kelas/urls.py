from django.conf.urls import patterns, url
from kelas import views

urlpatterns = patterns('kelas',
    url(r'^$', views.kelas, name='kelas'),
    url(r'^tambah/$', views.tambah_kelas, name='tambah_kelas'),
    url(r'^ubah/(?P<idKelas>\d+)/$', views.ubah_kelas, name='ubah_kelas'),
    url(r'^hapus/(?P<idKelas>\d+)/$', views.hapus_kelas, name='hapus_kelas'),
    url(r'^siswa/(?P<idKelas>\d+)/$', views.kelas_siswa, name='kelas_siswa'),
    url(r'^siswa/(?P<idKelas>\d+)/cetak/$', views.cetak_kelas_siswa, name='cetak_kelas_siswa'),
    url(r'^get_siswa/(?P<idJurusan>\d+)/$', views.get_siswa_json, name='get_siswa_json'),
)
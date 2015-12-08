from django.conf.urls import patterns, url, include
from kesiswaan import views
#from absensi import views
urlpatterns = patterns('kesiswaan',
    #url(r'^$', views.kesiswaan, name='kesiswaan'),
    url(r'^siswa/$', views.siswa, name='siswa'),
    url(r'^siswa/tambah/$', views.tambah_siswa, name='tambah_siswa'),
    url(r'^siswa/ubah/(?P<idSiswa>\d+)/$', views.ubah_siswa, name='ubah_siswa'),
    url(r'^siswa/hapus/(?P<idSiswa>\d+)/$', views.hapus_siswa, name='hapus_siswa'),
    url(r'^siswa/detil/(?P<idSiswa>\d+)/$', views.detilsiswa, name='detilsiswa'),
    url(r'^siswa/cetak/(?P<idSiswa>\d+)/$', views.cetaksiswa, name='cetaksiswa'),
    url(r'^absensi/', include('absensi.urlssiswa')),
    url(r'^kelas/', include('kelas.urls')),
)


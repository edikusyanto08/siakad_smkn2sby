from django.conf.urls import patterns, url, include
from kepegawaian import views

urlpatterns = patterns('kepegawaian',
    #url(r'^$', views.kepegawaian, name='kepegawaian'),
    url(r'^guru/$', views.guru, name='guru'),
    url(r'^guru/tambah/$', views.tambah_guru, name='tambah_guru'),
    url(r'^guru/ubah/(?P<idGuru>\d+)/$', views.ubah_guru, name='ubah_guru'),
    url(r'^guru/hapus/(?P<idGuru>\d+)/$', views.hapus_guru, name='hapus_guru'),
    url(r'^guru/detil/(?P<idGuru>\d+)/$', views.detilguru, name='detilguru'),
    url(r'^guru/cetak/(?P<idGuru>\d+)/$', views.cetakguru, name='cetakguru'),
    url(r'^absensi/', include('absensi.urlsguru')),
)


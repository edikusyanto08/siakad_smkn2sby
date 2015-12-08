from django.conf.urls import patterns, url
from jadwal import views

urlpatterns = patterns('kalender',
    url(r'^$', views.kalender, name='kalender'),
    url(r'^tambah/$', views.tambah_kegiatan, name='tambah_kegiatan'),
    url(r'^hapus/(?P<idKegiatan>\d+)/$', views.hapus_kegiatan, name='hapus_kegiatan'),
    url(r'^detil/(?P<idKegiatan>\d+)/$', views.detil_kegiatan, name='detil_kegiatan'),
)

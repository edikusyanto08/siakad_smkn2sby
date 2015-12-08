from django.conf.urls import patterns, url
from mapel import views

urlpatterns = patterns('kompetensi',
    url(r'^$', views.kompetensi, name='kompetensi'),
    url(r'^tambah/$', views.tambah_kompetensi, name='tambah_kompetensi'),
    url(r'^ubah/(?P<idKompetensi>\d+)/$', views.ubah_kompetensi, name='ubah_kompetensi'),
    url(r'^hapus/(?P<idKompetensi>\d+)/$', views.hapus_kompetensi, name='hapus_kompetensi'),
)
from django.conf.urls import patterns, url
from mapel import views

urlpatterns = patterns('mapel',
    url(r'^$', views.mapel, name='mapel'),
    url(r'^tambah/$', views.tambah_mapel, name='tambah_mapel'),
    url(r'^ubah/(?P<idMapel>\d+)/$', views.ubah_mapel, name='ubah_mapel'),
    url(r'^hapus/(?P<idMapel>\d+)/$', views.hapus_mapel, name='hapus_mapel'),
)
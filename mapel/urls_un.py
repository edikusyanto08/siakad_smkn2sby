from django.conf.urls import patterns, url
from mapel import views

urlpatterns = patterns('mapelun',
    url(r'^$', views.mapel_un, name='mapelun'),
    url(r'^tambah/$', views.tambah_un, name='tambah_mapelun'),
    url(r'^hapus/(?P<idMapelun>\d+)/$', views.hapus_un, name='hapus_mapelun'),
)
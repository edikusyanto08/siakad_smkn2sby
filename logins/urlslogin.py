from django.conf.urls import patterns, url
from logins import views

urlpatterns = patterns('user',
    url(r'^$', views.user, name='user'),
    #url(r'^tambah/$', views.tambah_user, name='tambah_user'),
    url(r'^reset/(?P<idUser>\d+)/$', views.reset_password, name='reset_password'),
    url(r'^blokir/(?P<idUser>\d+)/$', views.blokir_user, name='blokir_user'),
    url(r'^detil/(?P<Username>[-\w]+)/$', views.detil_user, name='detil_user'),
    url(r'^password/$', views.ubah_password, name='ubah_password'),
)
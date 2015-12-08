from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'siakad.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'logins.views.home', name="home"),
    url(r'^user/', include('logins.urlslogin')),
    url(r'^login/', 'logins.views.login_view', name="login"),
    url(r'^home/', 'logins.views.home', name="home"),
    url(r'^logout/', 'logins.views.logout_view', name="logout"),
    url(r'^data_master/', include('data_master.urls')),
    url(r'^jadwal/', include('jadwal.urls')),
    url(r'^kalender/', include('jadwal.urlskalender')),
    url(r'^kesiswaan/', include('kesiswaan.urls')),
    url(r'^kepegawaian/', include('kepegawaian.urls')),
    url(r'^laporan/', include('absensi.urls_laporan')),
    url(r'^penilaian/', include('penilaian.urls')),


    #url(r'^ortu/', include('users.urlsortu')),
)
#Jika mode debug true maka file static ditambahkan dlm url agar bisa diakses browser
#ini berlaku untuk tahap development, tahap produksi biarkan server yg menangani static file utk alasan keamanan
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
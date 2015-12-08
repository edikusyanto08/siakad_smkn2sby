from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.db.models import Q
from data_master.models import ThnAjaran
from kelas.models import Kelas, Kelas_Siswa
from django.contrib import messages
from absensi.models import AbsensiSiswa

# Create your views here.
def kesiswaan(request):
    page = "kesiswaan"
    pagegroups = "kesiswaan"
    heading = "Kesiswaan"
    title = heading+" | "
    breadcrumb = "<li><a href=/home/>Home</a></li>\
                <li class=active>Kesiswaan</li>"
    context = {"page":page,
               "pagegroups":pagegroups,
               "title":title,
               "heading":heading,
               "breadcrumb":breadcrumb,
               }
    return render(request, "kesiswaan/kesiswaan.html", context)

def siswa(request):
    if request.session['hak_akses'] !="siswa":
        if "q" in request.GET:
            keyword = request.GET['q']
            queryset = Q(nama_lengkap__icontains=keyword)\
                       | Q(NIS__exact=keyword)\
                       | Q(jurusan__nama_jurusan__icontains=keyword)\
                       | Q(tempat_lahir__icontains=keyword)\
                       | Q(alamat__icontains=keyword)
            datanya = Siswa.objects.filter(queryset)
        else:
            datanya=Siswa.objects.all()
        paginator = Paginator(datanya, 100)
        thnajaran = ThnAjaran.objects.all()
        if "hal" in request.GET:
            hal = request.GET['hal']
        else:
            hal = 1
        total_data = paginator.count
        try:
            siswanya = paginator.page(hal)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            siswanya = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            siswanya = paginator.page(paginator.num_pages)
        #kelasnya = Kelas_Siswa.objects.filter(tahun_ajaran=ThnAjaran.objects.latest('id'))
        pagegroups = 'kesiswaan'
        page = 'siswa'
        heading = "Data Siswa"
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li class=active>Data Siswa</li>"

        linkubah = "ubah/"
        linkhapus = "hapus/"
        context = {"siswanya": siswanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "title": title,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   #"kelasnya": kelasnya,
                   "linkubah": linkubah,
                   "linkhapus": linkhapus,
                   "total_data": total_data,
                   "thnajaran": thnajaran,
        }
        return render(request, 'kesiswaan/data_siswa.html', context )
    else:
        return render(request, "403.html", {} )

def tambah_siswa(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf":
        pagegroups = 'kesiswaan' #utk navigation
        page = 'siswa' #utk navigation
        heading = 'Tambah Data Siswa' #utk panel header
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/kesiswaan/siswa/>Data Siswa</a></li>\
                      <li class=active>Tambah Siswa</li>"
        linkback = "/kesiswaan/siswa"
        form = SiswaForm(request.POST or None, request.FILES or None)
        formOrtu = OrtuForm(request.POST or None, request.FILES or None)
        context = {"pagegroups": pagegroups,
                   "heading": heading,
                   "page": page,
                   "form": form,
                   "title": title,
                   "formOrtu": formOrtu,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,
                   }
        if form.is_valid() and formOrtu.is_valid():
            siswanya = form.save(commit=False)
            username = form.cleaned_data['NIS']
            password = form.cleaned_data['NIS']
            try:
                get_user, created = User.objects.get_or_create(username=username, first_name="siswa")
                #get_user=User.objects.get(username=username, first_name="siswa")
                get_user.set_password(password)
                get_user.save()
                siswanya.user_login = get_user
                siswanya.save()
                ortunya = formOrtu.save(commit=False)
                ortunya.siswa = siswanya
                ortunya.save()
                messages.success(request,'Data telah ditambahkan')
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
            return redirect('siswa')
        return render(request, 'kesiswaan/add_data.html', context)
    else:
        return render(request, "403.html", {} )

def ubah_siswa(request, idSiswa):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        siswas = get_object_or_404(Siswa, id=idSiswa)
        ortus = get_object_or_404(Ortu, siswa_id=idSiswa)
        pagegroups = 'kesiswaan'
        page = 'siswa'
        heading = 'Ubah Data Siswa'
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/kesiswaan/siswa/>Data Siswa</a></li>\
                      <li class=active>Ubah Data Siswa</li>"
        linkback = "/kesiswaan/siswa"
        form = SiswaForm(request.POST or None, request.FILES or None, instance= siswas)
        formOrtu = OrtuForm(request.POST or None, request.FILES or None, instance= ortus)
        context = {"pagegroups": pagegroups,
                   "heading": heading,
                   "page": page,
                   "form": form,
                   "title": title,
                   "formOrtu": formOrtu,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,
                   }
        if form.is_valid() and formOrtu.is_valid():
            username = form.cleaned_data['NIS']
            try:
                siswanya = form.save(commit=False)
                siswanya.save()
                ortunya = formOrtu.save(commit=False)
                ortunya.siswa = siswanya
                ortunya.save()
                get_user, created = User.objects.get_or_create(username=username, first_name="siswa")
                #get_user = User.objects.get(username=username)
                siswanya.user_login = get_user
                siswanya.save()
                messages.success(request,'Data berhasil diubah')
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal diubah. (%s)' %(err))
            return redirect('siswa')
        return render(request, 'kesiswaan/add_data.html', context)
    else:
        return render(request, "403.html", {} )

def hapus_siswa(request, idSiswa):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        try:
            siswas = get_object_or_404(Siswa, pk=idSiswa)
            user = get_object_or_404(User, username=siswas.NIS)
            siswas.delete()
            user.delete()
            messages.success(request,'Data telah dihapus')
            return redirect('siswa')
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))
            return redirect('siswa')
    else:
        return render(request, "403.html", {} )

def detilsiswa(request, idSiswa):
    if request.session['hak_akses'] !="siswa":
        datanya = Siswa.objects.all().filter(id=idSiswa)
        kelasnya = Kelas.objects.all().filter(siswa = idSiswa )
        absennya = AbsensiSiswa.objects.all().filter(siswa=idSiswa)
        nama = get_object_or_404(Siswa, pk=idSiswa)
    else:
        datanya = Siswa.objects.all().filter(id=request.session['id_user'])
        kelasnya = Kelas.objects.all().filter(siswa = request.session['id_user'] )
        nama = get_object_or_404(Siswa, pk=request.session['id_user'])
        absennya = AbsensiSiswa.objects.all().filter(siswa=request.session['id_user'])
    pagegroups = 'kesiswaan'
    page = 'siswa'
    breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/kesiswaan/siswa/>Data Siswa</a></li>\
                      <li class=active>Detil Siswa</li>"

    heading = nama.nama_lengkap
    title = heading+" | "
    context = {'datanya': datanya,
                   'pagegroups': pagegroups,
                   'page': page,
                   'heading':heading,
                   'title': title,
                   'breadcrumb': breadcrumb,
                   'kelasnya': kelasnya,
                   'absennya':absennya,
                   }
    return render(request, 'kesiswaan/detil_siswa.html', context )


def cetaksiswa(request, idSiswa):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        datanya = Siswa.objects.all().filter(id=idSiswa)
        kelasnya = Kelas.objects.all().filter(siswa = idSiswa )
        absennya = AbsensiSiswa.objects.all().filter(siswa=idSiswa)
        nama = get_object_or_404(Siswa, pk=idSiswa)
        heading = nama.nama_lengkap
        title = "Cetak Data Siswa "+heading+" | "
        context = {'datanya': datanya,
                   'heading':heading,
                   'title': title,
                   'kelasnya': kelasnya,
                   'absennya':absennya,
                   }
        return render(request,'kesiswaan/cetak_siswa.html', context)

#class Choices:
#    def _choices(self):
#        return [(e.id, e.description) for e in Kelas.objects.all()]
#    choices = property(_choices)
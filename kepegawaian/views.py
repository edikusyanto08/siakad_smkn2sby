from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from mapel.models import Mapel, MapelDiampu
# Create your views here.
def kepegawaian(request):
    page = "kepegawaian"
    pagegroups = "kepegawaian"
    heading = "Kepegawaian"
    title = heading+" | "
    breadcrumb = "<li><a href=/home/>Home</a></li>\
                <li class=active>Kepegawaian</li>"
    context = {"page":page,
               "pagegroups":pagegroups,
               "title":title,
               "heading":heading,
               "breadcrumb":breadcrumb,
               }
    return render(request, "kepegawaian/kepegawaian.html", context)

def guru(request):
    if request.session['hak_akses'] !="siswa":
        datanya = Guru.objects.all()
        pagegroups = 'kepegawaian'
        page = 'guru'
        heading = 'Data Guru'
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li class=active>Data Guru</li>"

        linkubah = "ubah/"
        linkhapus = "hapus/"
        context = {"datanya": datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "linkubah": linkubah,
                   "linkhapus": linkhapus,
        }
        return render(request, 'kepegawaian/data_guru.html', context )
    else:
        return render(request, "403.html", {} )

def tambah_guru(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        pagegroups = 'kepegawaian' #utk navigation
        page = 'guru' #utk navigation
        heading = 'Tambah Guru Baru' #utk panel header
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/kepegawaian/guru/>Data Guru</a></li>\
                      <li class=active>Tambah Guru</li>"
        linkback = "/kepegawaian/guru/"
        form = GuruForm(request.POST or None, request.FILES or None)
        context = {"pagegroups": pagegroups,
                   "heading": heading,
                   "page": page,
                   "form": form,
                   "title": title,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            username = form.cleaned_data['NIP']
            password = form.cleaned_data['NIP']
            akses = form.cleaned_data['hak_akses']
            try:
                User.objects.get_or_create(username=username, first_name=akses)
                get_user=User.objects.get(username=username)
                get_user.set_password(password)
                get_user.save()
                save_it.user_login = get_user
                save_it.save()
                messages.success(request,'Data telah ditambahkan.')
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
            return redirect('guru')
        return render(request, 'kepegawaian/add_data.html', context)
    else:
        return render(request, "403.html", {} )

def ubah_guru(request, idGuru):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        gurus = get_object_or_404(Guru, id=idGuru)
        pagegroups = 'kepegawaian'
        page = 'guru'
        heading = 'Ubah Data Guru'
        title = heading+" | "

        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/kepegawaian/guru/>Data Guru</a></li>\
                      <li class=active>Ubah Guru</li>"
        linkback = "/kepegawaian/guru/"
        form = GuruForm(request.POST or None, request.FILES or None, instance=gurus)
        context = {"pagegroups": pagegroups,
                   "heading": heading,
                   "page": page,
                   "title": title,
                   "form": form,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,

                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            username = form.cleaned_data['NIP']
            akses = form.cleaned_data['hak_akses']
            try:
                User.objects.get_or_create(username=username)
                get_user = User.objects.get(username=username)
                get_user.first_name = akses
                get_user.save()
                save_it.user_login = get_user
                save_it.save()
                messages.success(request,'Data berhasil diubah')
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal diubah. (%s)' %(err))
            return redirect('guru')
        return render(request, 'kepegawaian/add_data.html', context)
    else:
        return render(request, "403.html", {} )

def hapus_guru(request, idGuru):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        try:
            gurus = get_object_or_404(Guru, id=idGuru)
            user = get_object_or_404(User, username=idGuru)
            gurus.delete()
            user.delete()
            messages.success(request,'Data telah dihapus')
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))
        return redirect('guru')
    else:
        return render(request, "403.html", {} )

def detilguru(request, idGuru):
    if request.session['hak_akses'] !="siswa":
        datanya = Guru.objects.all().filter(id=idGuru)
        mapelnya = MapelDiampu.objects.all().filter(pengajar=idGuru)
        nama = get_object_or_404(Guru, pk=idGuru)
        pagegroups = 'kepegawaian'
        page = 'guru'
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/kepegawaian/guru/>Data Guru</a></li>\
                      <li class=active>Detil Guru</li>"

        heading = nama.nama_lengkap
        title ="Data "+heading
        context = {'datanya': datanya,
                   'mapelnya': mapelnya,
                   'pagegroups': pagegroups,
                   'page': page,
                   'heading':heading,
                   'title': title,
                   'breadcrumb': breadcrumb,

                   }
        return render(request, 'kepegawaian/detil_guru.html', context )
    else:
        return render(request, "403.html", {} )

def cetakguru(request, idGuru):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        datanya = Guru.objects.all().filter(id=idGuru)
        mapelnya = Mapel.objects.all().filter(pengajar=idGuru)
        nama = get_object_or_404(Guru, pk=idGuru)
        heading = nama.nama_lengkap
        title = heading+" | "
        context = {'datanya': datanya,
                   'heading':heading,
                   'title': title,
                   'mapelnya': mapelnya,
                   }
        return render(request,'kepegawaian/cetak_guru.html', context)
    else:
        return render(request, "403.html", {} )



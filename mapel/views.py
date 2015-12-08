from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
# Create your views here.
def mapel(request):
    if request.session['hak_akses'] !="siswa" and request.session['hak_akses'] !="guru":
        datanya = Mapel.objects.all().order_by('type_mapel')
        pengajar = MapelDiampu.objects.all()
        pagegroups = "data"
        page = "mapel"
        breadcrumb = "<li><a href=/home/>Home</a></li><li class=active>Data Mapel</li>"
        heading = "Data Mata Pelajaran"
        title = heading+" | "

        linkubah = "ubah/"
        linkhapus = "hapus/"

        context = {"datanya": datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "pengajar": pengajar,
                   "linkubah": linkubah,
                   "linkhapus": linkhapus,

        }
        return render(request, "mapel/data_mapel.html", context )
    else:
        return render(request, "403.html", {} )

def tambah_mapel(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka" :
        pagegroups = "data" #utk navigation
        page = "mapel" #utk navigation
        heading = "Tambah Mata Pelajaran" #utk panel header
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>"\
                     "<li><a href=/data_master/mapel/>Data Mapel</a></li>"\
                     "<li class=active>Tambah Mapel</li>"
        linkback = '/data_master/mapel/'

        form = MapelForm(request.POST or None, request.FILES or None)
        form.fields['pengajar'].queryset = Guru.objects.filter(hak_akses="guru")
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
            gurunya = form.cleaned_data['pengajar']
            try:
                save_it.save()
                for guru in gurunya:
                    baru = MapelDiampu(mapel=save_it, pengajar=guru)
                    baru.save()
                messages.success(request,"Data berhasil ditambahkan")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
            return redirect('mapel')

        return render(request, "mapel/add_mapel.html", context)
    else:
        return render(request, "403.html", {} )

def ubah_mapel(request, idMapel):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka" :
        datannya = get_object_or_404(Mapel, id=idMapel)
        pagegroups = "data"
        page = "mapel"
        heading = "Ubah Mata Pelajaran"
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/data_master/mapel/>Data Mapel</a></li>\
                      <li class=active>Ubah Mapel</li>"
        linkback = '/data_master/mapel/'
        form = MapelForm(request.POST or None, request.FILES or None, instance=datannya)
        form.fields['pengajar'].queryset = Guru.objects.filter(hak_akses="guru")
        context = {"heading": heading,
                   "pagegroups": pagegroups,
                   "page": page,
                   "form":form,
                   "title": title,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            gurunya = form.cleaned_data['pengajar']
            changed = 0
            jml = gurunya.count()
            for data in gurunya:
                try:
                    MapelDiampu.objects.get(mapel=save_it, pengajar=data)
                except:
                    changed +=1
            try:
                save_it.save()
                if changed > 0 or jml != MapelDiampu.objects.filter(mapel=save_it).count():
                    for guru in gurunya:
                        MapelDiampu.objects.get_or_create(mapel=save_it, pengajar=guru)
                    hapus = MapelDiampu.objects.filter(mapel=save_it).exclude(pengajar__in=gurunya)
                    hapus.delete()
                    #messages.warning(request,"Data pengajar telah dirubah, hal ini berpengaruh terhadap semua data jadwal yang berhubungan dengan mapel yang bersangkutan.\
                    # Mohon periksa kembali ")
                messages.success(request,"Data telah diubah")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal diubah. (%s)' %(err))
            return redirect('mapel')

        return render(request, "mapel/add_mapel.html", context)
    else:
        return render(request, "403.html", {} )

def hapus_mapel(request, idMapel):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka" :
        datanya = get_object_or_404(Mapel, pk=idMapel)
        try:
            datanya.delete()
            messages.success(request,"Data telah dihapus")
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))

        return redirect("mapel")
    else:
        return render(request, "403.html", {} )

def kompetensi(request):
    if request.session['hak_akses'] !="siswa" and request.session['hak_akses'] !="guru":
        datanya = KompetensiKejuruan.objects.all()
        pagegroups = "data"
        page = "kompetensi"
        breadcrumb = "<li><a href=/home/>Home</a></li><li class=active>Data Kompetensi Kejuruan</li>"
        heading = "Data Kompetensi Kejuruan"
        title = heading+" | "

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
        return render(request, "mapel/data_kompetensi.html", context )
    else:
        return render(request, "403.html", {} )

def tambah_kompetensi(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka" :
        pagegroups = "data" #utk navigation
        page = "kompetensi" #utk navigation
        heading = "Tambah Kompetensi Kejuruan" #utk panel header
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>"\
                     "<li><a href=/data_master/kompetensi/>Data Kompetensi Kejuruan</a></li>"\
                     "<li class=active>Tambah Kompetensi Kejuruan</li>"
        linkback = '/data_master/kompetensi/'
        form = KompetensiKejuruanForm(request.POST or None, request.FILES or None)
        form.fields['mapel_induk'].queryset = Mapel.objects.filter(type_mapel__icontains="Dasar")
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
            try:
                save_it.save()
                messages.success(request,"Data berhasil ditambahkan")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
            return redirect('kompetensi')
        return render(request, "mapel/add_mapel.html", context)
    else:
        return render(request, "403.html", {} )

def ubah_kompetensi(request, idKompetensi):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka" :
        datannya = get_object_or_404(KompetensiKejuruan, id=idKompetensi)
        pagegroups = "data"
        page = "kompetensi"
        heading = "Ubah Kompetensi Kejuruan"
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/data_master/kompetensi/>Data Kompetensi Kejuruan</a></li>\
                      <li class=active>Ubah Kompetensi Kejuruan</li>"
        linkback = '/data_master/kompetensi/'
        form = KompetensiKejuruanForm(request.POST or None, request.FILES or None, instance=datannya)
        form.fields['mapel_induk'].queryset = Mapel.objects.filter(type_mapel__icontains="dasar")
        context = {"heading": heading,
                   "pagegroups": pagegroups,
                   "page": page,
                   "form":form,
                   "title": title,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,

                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                messages.success(request,"Data telah diubah")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal diubah. (%s)' %(err))
            return redirect('kompetensi')

        return render(request, "mapel/add_mapel.html", context)
    else:
        return render(request, "403.html", {} )

def hapus_kompetensi(request, idKompetensi):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka" :
        datanya = get_object_or_404(KompetensiKejuruan, pk=idKompetensi)
        try:
            datanya.delete()
            messages.success(request,"Data telah dihapus")
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))
        return redirect("kompetensi")
    else:
        return render(request, "403.html", {} )

def mapel_un(request):
    if request.session['hak_akses'] !="siswa" and request.session['hak_akses'] !="guru":
        pagegroups = "data"
        page = "mapelun"
        breadcrumb = "<li><a href=/home/>Home</a></li><li class=active>Data Mapel UN</li>"
        heading = "Data Mata Pelajaran Ujian Nasional"
        title = heading+" | "
        datanya = MapelUN.objects.all()
        context = {"heading": heading,
                   "pagegroups": pagegroups,
                   "page": page,
                   "title": title,
                   "breadcrumb": breadcrumb,
                   "datanya": datanya,
                   }
        return render(request, "mapel/mapel_un.html", context)
    else:
        return render(request, "403.html", {} )

def tambah_un(request):
    if request.session['hak_akses'] == "waka" or request.session['hak_akses'] == "Admin":
        pagegroups = "data"
        page = "mapelun"
        breadcrumb = "<li><a href=/home/>Home</a></li>"\
                     "<li><a href=/data_master/mapelun/>Data Mapel UN</a></li>"\
                     "<li class=active>Tambah Mapel</li>"
        heading = "Tambah Mata Pelajaran Ujian Nasional"
        title = heading+" | "
        linkback = '/data_master/mapelun/'
        mapelun = MapelUN.objects.all()
        form = MapelUNForm(request.POST or None, request.FILES or None)
        form.fields['mapel'].queryset = Mapel.objects.filter(jurusan=None).exclude(id__in=[mapel.mapel.id for mapel in mapelun])
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
            try:
                save_it.save()
                messages.success(request,"Data berhasil ditambahkan")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
            return redirect('mapelun')

        return render(request, "mapel/add_mapel.html", context)
    else:
        return render(request, "403.html", {} )

def hapus_un(request, idMapelun):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka" :
        datanya = get_object_or_404(MapelUN, pk=idMapelun)
        try:
            datanya.delete()
            messages.success(request,"Data telah dihapus")
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))

        return redirect("mapelun")
    else:
        return render(request, "403.html", {} )
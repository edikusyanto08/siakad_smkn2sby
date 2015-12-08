from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.utils.html import escape
# Create your views here.
# jabatan ----------------------------------------------------------------------------------------------
ThnAjaran.objects.get_or_create(tahun_ajaran="2014/2015")

def data_master(request):
    page = "data"
    pagegroups = "data"
    heading = "Data Master"
    title = heading+" | "
    breadcrumb = "<li><a href=/home/>Home</a></li>\
                <li class=active>Data Master</li>"
    context = {"page":page,
               "pagegroups":pagegroups,
               "title":title,
               "heading":heading,
               "breadcrumb":breadcrumb,
               }
    return render(request, "data_master/data_master.html", context)

def jabatan(request):
    if request.session['hak_akses'] !="siswa" and request.session['hak_akses'] !="guru" :
        datanya = Jabatan.objects.all()
        pagegroups = "data"
        page = "jabatan"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li class=active>Data Jabatan</li>"
        heading = "Data Jabatan"
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
        return render(request, "data_master/view_data.html", context )
    else:
        return render(request, "403.html", {} )

def tambah_jabatan(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        pagegroups = "data" #utk navigation
        page = "jabatan" #utk navigation
        heading = "Tambah Jabatan" #utk panel header
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                     <li><a href=/data_master/jabatan/>Data Jabatan</a></li>\
                     <li class=active>Tambah Jabatan</li>"
        linkback = "/data_master/jabatan/"
        form = JabatanForm(request.POST or None, request.FILES or None)
        context = {"pagegroups": pagegroups,
                   "heading": heading,
                   "title": title,
                   "page": page,
                   "form": form,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,

                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                idnya = escape(save_it._get_pk_val())
                valuenya = escape(save_it)
                rendernya = "onload=refreshAndClose()"
                context={"rendernya": rendernya,
                         "idnya":idnya,
                         "valuenya":valuenya,
                        }
                if "done" in request.GET:
                    return render(request, 'data_master/popup_add.html', context)
                else:
                    messages.success(request,'Data telah ditambahkan')
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
            return redirect("jabatan")

        if "_popup" in request.GET:
            return render(request, "data_master/popup_add.html", context)
        else:
            return render(request, "data_master/add_data.html", context)
    else:
        return render(request, "403.html", {} )

def ubah_jabatan(request, idData):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        datanya = get_object_or_404(Jabatan, id=idData)
        pagegroups = "data"
        page = "jabatan"
        heading = "Ubah Jabatan"
        title = heading+" | "
        linkback = "/data_master/jabatan/"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a href=/data_master/jabatan/>Data Jabatan</a></li>\
                    <li class=active>Ubah Jabatan</li>"
        form = JabatanForm(request.POST or None, request.FILES or None, instance=datanya)
        context = {"pagegroups": pagegroups,
                   "heading": heading,
                   "title": title,
                   "page": page,
                   "form": form,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                messages.success(request,"Data berhasil diubah.")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal diubah. (%s)' %(err))
            return redirect('jabatan')

        return render(request, "data_master/add_data.html", context)
    else:
        return render(request, "403.html", {} )

def hapus_jabatan(request, idData):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        datanya = get_object_or_404(Jabatan, pk=idData)
        try:
            datanya.delete()
            messages.success(request,"Data telah dihapus")
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))

        return redirect('jabatan')
    else:
            return render(request, "403.html", {} )

# pangkat ----------------------------------------------------------------------------------------------
def pangkat(request):
    if request.session['hak_akses'] !="siswa" and request.session['hak_akses'] !="guru":
        datanya = Pangkat.objects.all()
        pagegroups = "data"
        page = "pangkat"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                     <li class=active>Data Pangkat</li>"
        heading = "Data Pangkat"
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
        return render(request, "data_master/view_data.html", context )
    else:
        return render(request, "403.html", {} )

def tambah_pangkat(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        pagegroups = "data" #utk navigation
        page = "pangkat" #utk navigation
        heading = "Tambah Pangkat" #utk panel header
        title = heading+" | "
        linkback = "/data_master/pangkat/"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a href=/data_master/pangkat/>Data Pangkat</a></li>\
                    <li class=active>Tambah Pangkat</li>"
        form = PangkatForm(request.POST or None, request.FILES or None)
        context = {"pagegroups": pagegroups,
                   "heading": heading,
                   "title": title,
                   "page": page,
                   "form": form,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,

                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                idnya = escape(save_it._get_pk_val())
                valuenya = escape(save_it)
                rendernya = "onload=refreshAndClose()"
                context={"rendernya": rendernya,
                         "idnya":idnya,
                         "valuenya":valuenya,
                        }
                if "done" in request.GET:
                    return render(request, 'data_master/popup_add.html', context)
                else:
                    messages.success(request,'Data telah ditambahkan')
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
            return redirect("pangkat")

        if "_popup" in request.GET:
            return render(request, "data_master/popup_add.html", context)
        else:
            return render(request, "data_master/add_data.html", context)
    else:
        return render(request, "403.html", {} )

def ubah_pangkat(request, idData):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        datanya = get_object_or_404(Pangkat, id=idData)
        pagegroups = "data"
        page = "pangkat"
        heading = "Ubah Pangkat"
        title = heading+" | "
        linkback = "/data_master/pangkat/"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a href=/data_master/pangkat/>Data Pangkat</a></li>\
                    <li class=active>Ubah Pangkat</li>"
        form = PangkatForm(request.POST or None, request.FILES or None, instance=datanya)
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
            try:
                save_it.save()
                messages.success(request,"Data berhasil diubah.")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal diubah. (%s)' %(err))
            return redirect('pangkat')

        return render(request, "data_master/add_data.html", context)
    else:
        return render(request, "403.html", {} )

def hapus_pangkat(request, idData):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        datanya = get_object_or_404(Pangkat, pk=idData)
        try:
            datanya.delete()
            messages.success(request,"Data telah dihapus.")
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))
        return redirect('pangkat')
    else:
        return render(request, "403.html", {} )


# thnajaran ----------------------------------------------------------------------------------------------
def thnajaran(request):
    if request.session['hak_akses'] !="siswa" and request.session['hak_akses'] !="guru":
        datanya = ThnAjaran.objects.all()
        pagegroups = "data"
        page = "thnajaran"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li class=active>Data Tahun Ajaran</li>"
        heading = "Data Tahun Ajaran"
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

        return render(request, "data_master/view_data.html", context )
    else:
        return render(request, "403.html", {} )

def tambah_thnajaran(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        pagegroups = "data" #utk navigation
        page = "thnajaran" #utk navigation
        heading = "Tambah Tahun Ajaran" #utk panel header
        title = heading+" | "
        linkback = "/data_master/tahun_ajaran/"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a href=/data_master/tahun_ajaran/>Data Tahun Ajaran</a></li>\
                    <li class=active>Tambah Tahun Ajaran</li>"
        form = ThnAjaranForm(request.POST or None, request.FILES or None)
        context = {"pagegroups": pagegroups,
                   "heading": heading,
                   "title": title,
                   "page": page,
                   "form": form,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback

                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                idnya = escape(save_it._get_pk_val())
                valuenya = escape(save_it)
                rendernya = "onload=refreshAndClose()"
                context={"rendernya": rendernya,
                         "idnya":idnya,
                         "valuenya":valuenya,
                        }
                if "done" in request.GET:
                    return render(request, 'data_master/popup_add.html', context)
                else:
                    messages.success(request,'Data telah ditambahkan')
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
            return redirect("thnajaran")

        if "_popup" in request.GET:
            return render(request, "data_master/popup_add.html", context)
        else:
            return render(request, "data_master/add_data.html", context)
    else:
        return render(request, "403.html", {} )

def ubah_thnajaran(request, idData):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        datanya = get_object_or_404(ThnAjaran, id=idData)
        pagegroups = "data"
        page = "thnajaran"
        heading = "Ubah Tahun Ajaran"
        title = heading+" | "
        linkback = "/data_master/tahun_ajaran/"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a href=/data_master/tahun_ajaran/>Data Tahun Ajaran</a></li>\
                    <li class=active>Ubah Tahun Ajaran</li>"
        form = ThnAjaranForm(request.POST or None, request.FILES or None, instance=datanya)
        context = {"pagegroups": pagegroups,
                   "heading": heading,
                   "title": title,
                   "page": page,
                   "form": form,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,

        }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                messages.success(request,"Data berhasil diubah")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal diubah. (%s)' %(err))
            return redirect('thnajaran')

        return render(request, "data_master/add_data.html", context)
    else:
        return render(request, "403.html", {} )

def hapus_thnajaran(request, idData):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        datanya = get_object_or_404(ThnAjaran, pk=idData)
        if ThnAjaran.objects.count() > 1:
            try:
                datanya.delete()
                messages.success(request,"Data telah dihapus")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))
        else:
            messages.error(request,"Minimal harus ada tahun ajaran.")
        return redirect('thnajaran')
    else:
        return render(request, "403.html", {} )

# jurusan ----------------------------------------------------------------------------------------------
def jurusan(request):
    if request.session['hak_akses'] !="siswa" and request.session['hak_akses'] !="guru":
        datanya = Jurusan.objects.all()
        pagegroups = "data"
        page = "jurusan"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li class=active>Data Jurusan</li>"
        heading = "Data Jurusan"
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
        return render(request, "data_master/view_data.html", context )
    else:
        return render(request, "403.html", {} )

def tambah_jurusan(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        pagegroups = "data" #utk navigation
        page = "jurusan" #utk navigation
        heading = "Tambah Jurusan" #utk panel header
        title = heading+" | "
        linkback = "/data_master/jurusan/"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a href=/data_master/jurusan/>Data Jurusan</a></li>\
                     <li class=active>Tambah Jurusan</li>"
        form = JurusanForm(request.POST or None, request.FILES or None)
        context = {"pagegroups": pagegroups,
                   "heading": heading,
                   "page": page,
                   "form": form,
                   "breadcrumb": breadcrumb,
                   "title": title,
                   "linkback": linkback,

                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                idnya = escape(save_it._get_pk_val())
                valuenya = escape(save_it)
                rendernya = "onload=refreshAndClose()"
                context={"rendernya": rendernya,
                         "idnya":idnya,
                         "valuenya":valuenya,
                        }
                if "done" in request.GET:
                    return render(request, 'data_master/popup_add.html', context)
                else:
                    messages.success(request,'Data telah ditambahkan')
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
            return redirect("jurusan")

        if "_popup" in request.GET:
            return render(request, "data_master/popup_add.html", context)
        else:
            return render(request, "data_master/add_data.html", context)
    else:
        return render(request, "403.html", {} )

def ubah_jurusan(request, idData):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        datanya = get_object_or_404(Jurusan, id=idData)
        pagegroups = "data"
        page = "jurusan"
        heading = "Ubah Jurusan"
        title = heading+" | "
        linkback = "/data_master/jurusan/"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a href=/data_master/jurusan/>Data Jurusan</a></li>\
                    <li class=active>Ubah Jurusan</li>"
        form = JurusanForm(request.POST or None, request.FILES or None, instance=datanya)
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
            try:
                save_it.save()
                messages.success(request,"Data berhasil diubah.")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal diubah. (%s)' %(err))
            return redirect('jurusan')

        return render(request, "data_master/add_data.html", context)
    else:
        return render(request, "403.html", {} )

def hapus_jurusan(request, idData):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        datanya = get_object_or_404(Jurusan, pk=idData)
        try:
            datanya.delete()
            messages.success(request,"Data telah dihapus")
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))

        return redirect('jurusan')
    else:
        return render(request, "403.html", {} )

def ruang(request):
    if request.session['hak_akses'] !="siswa" and request.session['hak_akses'] !="guru":
        datanya = Ruang.objects.all()
        pagegroups = "data"
        page = "ruang"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li class=active>Data Ruang</li>"
        heading = "Data Ruang"
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
        return render(request, "data_master/view_data.html", context )
    else:
        return render(request, "403.html", {} )

def tambah_ruang(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        pagegroups = "data" #utk navigation
        page = "ruang" #utk navigation
        heading = "Tambah Ruang" #utk panel header
        title = heading+" | "
        linkback = "/data_master/ruang/"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a href=/data_master/ruang/>Data Ruang</a></li>\
                    <li class=active>Tambah Ruang</li>"
        form = RuangForm(request.POST or None, request.FILES or None)
        context = {"pagegroups": pagegroups,
                   "heading": heading,
                   "title": title,
                   "page": page,
                   "form": form,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback

                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                idnya = escape(save_it._get_pk_val())
                valuenya = escape(save_it)
                rendernya = "onload=refreshAndClose()"
                context={"rendernya": rendernya,
                         "idnya":idnya,
                         "valuenya":valuenya,
                        }
                if "done" in request.GET:
                    return render(request, 'data_master/popup_add.html', context)
                else:
                    messages.success(request,'Data telah ditambahkan')
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
            return redirect("ruang")

        if "_popup" in request.GET:
            return render(request, "data_master/popup_add.html", context)
        else:
            return render(request, "data_master/add_data.html", context)
    else:
        return render(request, "403.html", {} )

def ubah_ruang(request, idData):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        datanya = get_object_or_404(Ruang, id=idData)
        pagegroups = "data"
        page = "ruang"
        heading = "Ubah Ruang"
        title = heading+" | "
        linkback = "/data_master/ruang/"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a href=/data_master/ruang/>Data Ruang</a></li>\
                    <li class=active>Ubah Ruang</li>"
        form = RuangForm(request.POST or None, request.FILES or None, instance=datanya)
        context = {"pagegroups": pagegroups,
                   "heading": heading,
                   "title": title,
                   "page": page,
                   "form": form,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,

        }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                messages.success(request,"Data berhasil diubah")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal diubah. (%s)' %(err))
            return redirect('ruang')

        return render(request, "data_master/add_data.html", context)
    else:
        return render(request, "403.html", {} )

def hapus_ruang(request, idData):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        datanya = get_object_or_404(Ruang, pk=idData)
        try:
            datanya.delete()
            messages.success(request,"Data telah dihapus")
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))
        return redirect('ruang')
    else:
        return render(request, "403.html", {} )

from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.db.models import Q
import json
from django.http import HttpResponse
# Create your views here.

def kelas(request):
    if request.session['hak_akses'] !="siswa":
        if "thn_ajaran" in request.POST and request.POST['thn_ajaran'] !="0":
            thnajaran_id=request.POST['thn_ajaran']
        else:
            thnajaran_id=ThnAjaran.objects.latest('id').id
        datanya = Kelas.objects.all().filter(tahun_ajaran = thnajaran_id)
        if not request.session['kelas_siswa']:
            request.session['kelas_siswa'] = [siswa.siswa.id for siswa in Kelas_Siswa.objects.filter(tahun_ajaran = thnajaran_id)]
        thnajaran = ThnAjaran.objects.all()
        pagegroups = "kesiswaan"
        page = "kelas"
        tahun = "Tahun Ajaran "+ThnAjaran.objects.get(id=thnajaran_id).tahun_ajaran
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li class=active>Data Kelas</li>"
        heading = "Data Kelas Tersedia "+tahun
        title = "Data Kelas Tersedia | "
        linkubah = "ubah/"
        linkhapus = "hapus/"
        context = {"datanya": datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "thnajaran": thnajaran,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "tahun":tahun,

                   "linkubah": linkubah,
                   "linkhapus": linkhapus,

                   }

        return render(request, "kelas/data_kelas.html",context )
    else:
        return render(request, "403.html", {} )

def get_siswa_json(request, idJurusan):
    jurusan = Jurusan.objects.get(id=idJurusan)
    kelas_siswa = Kelas_Siswa.objects.filter(tahun_ajaran=ThnAjaran.objects.latest('id'))
    siswanya = Siswa.objects.filter(tanggal_lulus=None, jurusan=jurusan).exclude(id__in =[kelas.siswa.id for kelas in kelas_siswa])
    siswa_dict = {}
    for siswa in siswanya:
        siswa_dict[siswa.id] = siswa.nama_lengkap
    return HttpResponse(json.dumps(siswa_dict), content_type="application/json")

def tambah_kelas(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        pagegroups = "kesiswaan"
        page = "kelas"
        heading = "Tambah Kelas"
        title = "Tambah Kelas | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a onclick=self.history.back()>Data Kelas</a></li>\
                    <li class=active>Tambah Kelas</li>"
        linkback = "/kesiswaan/kelas/"

        form = KelasForm(request.POST or None, request.FILES or None)
        kelas_guru = Kelas.objects.filter(tahun_ajaran=ThnAjaran.objects.latest('id'))
        #form.fields['tahun_ajaran'].queryset = ThnAjaran.objects.latest('id')
        form.fields['tahun_ajaran'].initial = ThnAjaran.objects.latest('id')
        form.fields['wali_kelas'].queryset = Guru.objects.filter(hak_akses="guru").exclude(id__in=[pengajar.wali_kelas.id for pengajar in kelas_guru])
        form.fields['siswa'].queryset = Siswa.objects.filter(tanggal_lulus=None).exclude(id__in = request.session['kelas_siswa'])
        context = {"pagegroups": pagegroups,
                   "page": page,
                   "heading": heading,
                   "title": title,
                   "form": form,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,

                   }
        if form.is_valid():
            kelasnya = form.save(commit=False)
            kelasnya.save()
            siswanya = form.cleaned_data['siswa']
            for siswas in siswanya:
                try:
                    baru = Kelas_Siswa(siswa=siswas, tahun_ajaran=kelasnya.tahun_ajaran, kelas=kelasnya)
                    baru.save()
                    request.session['kelas_siswa'] = []
                except:
                    messages.error(request, "Duplikat data! %s sudah mendapatkan kelas" %(siswas))
            messages.success(request,"Data telah Ditambahkan")
            return redirect('kelas')

        return render(request, "kelas/add_kelas.html", context)
    else:
        return render(request, "403.html", {} )

def ubah_kelas(request, idKelas):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        kelass = get_object_or_404(Kelas, pk=idKelas)
        request.session['idkelas'] = kelass.id
        pagegroups = "kesiswaan"
        page = "kelas"
        heading = "Ubah Kelas"
        title = "Ubah Kelas | "

        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a onclick=self.history.back()>Data Kelas</a></li>\
                    <li class=active>Tambah Kelas</li>"
        linkback = "/kesiswaan/kelas/"
        form = KelasForm(request.POST or None, request.FILES or None, instance= kelass)
        #form.fields['tahun_ajaran'].queryset = ThnAjaran.objects.latest('id')
        form.fields['tahun_ajaran'].initial = ThnAjaran.objects.latest('id')
        form.fields['siswa'].queryset = Siswa.objects.filter(tanggal_lulus=None, jurusan=kelass.jurusan)#.exclude(id__in = request.session['kelas_siswa'])
        context = {"pagegroups": pagegroups,
                   "page": page,
                   "heading": heading,
                   "title": title,
                   "form": form,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,
                   }
        if form.is_valid():
            kelasnya = form.save(commit=False)
            kelasnya.save()
            #hapus = Kelas_Siswa.objects.filter(kelas=kelasnya)
            #hapus.delete()
            siswanya = form.cleaned_data['siswa']
            data = Kelas_Siswa.objects.filter(kelas__id=idKelas).exclude(id__in = [sis.id for sis in siswanya])
            data.delete()
            for siswas in siswanya:
                try:
                    Kelas_Siswa.objects.get_or_create(siswa=siswas, tahun_ajaran=kelasnya.tahun_ajaran, kelas=kelasnya)
                    request.session['kelas_siswa'] = []
                except BaseException, err:
                    messages.error(request, "Terjadi kesalahan %s" %(err))
            messages.success(request,"Data telah diubah")
            return redirect('kelas')

        return render(request, "kelas/add_kelas.html", context)
    else:
        return render(request, "403.html", {} )

def hapus_kelas(request, idKelas):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        kelass = get_object_or_404(Kelas, pk=idKelas)
        kelass.delete()
        request.session['kelas_siswa'] = []
        messages.success(request,"Data telah dihapus")
        return redirect("kelas")
    else:
        return render(request, "403.html", {} )

def kelas_siswa(request, idKelas):
    datanya = Siswa.objects.filter(kelas_siswa__kelas=idKelas)
    pagegroups = "kesiswaan"
    page = "kelas"
    kelasnya = Kelas.objects.get(id=idKelas)
    heading = "Data Siswa Kelas <font color=#00ff00><i>"\
              +kelasnya.nama_kelas+"</i></font> Tahun Ajaran <font color=#00ff00><i>"\
              +kelasnya.tahun_ajaran.tahun_ajaran+"</i></font>"
    title = "Data Siswa  Kelas "+kelasnya.nama_kelas+" Tahun Ajaran "+kelasnya.tahun_ajaran.tahun_ajaran+" | "
    breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a onclick=self.history.back()>Data Kelas</a></li>\
                    <li class=active>Daftar Siswa Dalam Kelas</li>"

    context = {"pagegroups": pagegroups,
               "page": page,
               "heading": heading,
               "title": title,
               "breadcrumb": breadcrumb,
               "datanya": datanya,

               }
    return render(request, "kelas/kelas_siswa.html", context)

def cetak_kelas_siswa(request, idKelas):
    datanya = Siswa.objects.filter(kelas_siswa__kelas=idKelas)
    kelasnya = Kelas.objects.get(id=idKelas)
    heading = "Data Siswa Kelas <font color=#00ff00><i>"\
              +kelasnya.nama_kelas+"</i></font> Tahun Ajaran <font color=#00ff00><i>"\
              +kelasnya.tahun_ajaran.tahun_ajaran+"</i></font>"
    title = "Data Siswa Kelas "+kelasnya.nama_kelas+" Tahun Ajaran "+kelasnya.tahun_ajaran.tahun_ajaran+" | "
    context = {
                "kelasnya": kelasnya,
               "heading": heading,
               "title": title,
               "datanya": datanya,

               }
    return render(request, "kelas/cetak_kelas_siswa.html", context)
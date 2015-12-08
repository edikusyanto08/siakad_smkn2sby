from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from datetime import datetime
from penilaian.models import Periode
from django.db.models import Q

# Create your views here.
def kalender(request):
    page = "kalender"
    title = "Kalender Akademik | "
    breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li class=active>Kalender Akademik</li>"
    waktu = datetime.now().date()
    kegiatannya = Kegiatan.objects.all()
    kegiatan_bulan_ini = Kegiatan.objects.filter(tgl_mulai__month=datetime.now().month)
    form = KegiatanForm(request.POST or None, request.FILES or None)
    context = {"kegiatannya": kegiatannya,
               "kegiatan_bulan_ini":kegiatan_bulan_ini,
               "page": page,
               "title":title,
               "waktu":waktu,
               "breadcrumb": breadcrumb,
               "form":form,
               }
    if form.is_valid():
        save_it = form.save(commit=False)
        try:
            save_it.save()
            messages.success(request,"Kegiatan telah ditambahkan")
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
        return redirect('kalender')
    return render(request, "jadwal/kalender.html", context )

def detil_kegiatan(request,idKegiatan):
    kegiatan = Kegiatan.objects.get(id=idKegiatan)
    page = "kalender"
    heading = "Detil Kegiatan"
    title = "Detil Kegiatan | "
    breadcrumb = "<li><a href=/home/>Home</a></li>\
                <li><a href=/kalender/>Kalender Akademik</a></li>\
                <li class=active>Detil Kegiatan</li>"
    linkhapus = "/kalender/hapus/"+idKegiatan


    form = KegiatanForm(request.POST or None, request.FILES or None, instance=kegiatan)
    context = {"page": page,
                "heading": heading,
                "title": title,
                "form": form,
                 "breadcrumb": breadcrumb,
                 "linkhapus":linkhapus,
                }
    if form.is_valid():
        save_it = form.save(commit=False)
        try:
            save_it.save()
            messages.success(request,"Kegiatan berhasil diubah")
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal diubah. (%s)' %(err))
        return redirect('kalender')
    return render(request, "jadwal/detil_kegiatan.html", context)

def tambah_kegiatan(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka" :
        page = "kalender"
        heading = "Tambah Kegiatan"
        title = "Tambah Kegiatan | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/kalender/>Kalender Akademik</a></li>\
                      <li class=active>Tambah Kegiatan</li>"
        linkback = "self.history.back()"
        form = KegiatanForm(request.POST or None, request.FILES or None)
        context = {"page": page,
                   "heading": heading,
                   "title": title,
                   "form": form,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                messages.success(request,"Kegiatan telah ditambahkan")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
            return redirect('kalender')
        return render(request, "jadwal/add_data.html", context)
    else:
        return render(request, "403.html", {} )


def hapus_kegiatan(request, idKegiatan):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka" :
        datanya = get_object_or_404(Kegiatan, pk=idKegiatan)
        try:
            datanya.delete()
            messages.success(request,"Data telah dihapus")
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))
        return redirect("kalender")
    else:
        return render(request, "403.html", {} )




def waktu(request):
    if request.session['hak_akses'] !="siswa" or request.session['hak_akses'] !="guru":
        datanya = Waktu.objects.all()
        pagegroups = "jadwalkbm"
        page = "waktu"
        breadcrumb = "<li><a href=/home/>Home</a></li><li class=active>Jam KBM</li>"
        heading = "Data Jam KBM Tersedia"
        title = "Data Jam KBM Tersedia | "


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
        return render(request, "jadwal/data_waktu.html",context )
    else:
        return render(request, "403.html", {} )


def tambah_waktu(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka" :
        pagegroups = "jadwalkbm"
        page = "waktu"
        heading = "Tambah Jam KBM"
        title = "Tambah Jam KBM | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/jadwal/waktu/>Data Jam KBM</a></li>\
                      <li class=active>Tambah Jam KBM</li>"
        linkback = "self.history.back()"

        form = WaktuForm(request.POST or None, request.FILES or None)
        context = {"pagegroups": pagegroups,
                   "page": page,
                   "heading": heading,
                   "title": title,
                   "form": form,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                messages.success(request,"Data telah ditambahkan")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
            return redirect('waktu')
        return render(request, "jadwal/add_data.html", context)
    else:
        return render(request, "403.html", {} )

def ubah_waktu(request, idWaktu):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka" :
        datanya = get_object_or_404(Waktu, pk=idWaktu)
        pagegroups = "jadwalkbm"
        page = "waktu"
        heading = "Ubah Jam KBM"
        title = "Ubah Jam KBM | "

        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/jadwal/waktu/>Data Jam KBM</a></li>\
                      <li class=active>Ubah Jam KBM</li>"
        linkback = "self.history.back()"
        form = WaktuForm(request.POST or None, request.FILES or None, instance= datanya)
        context = {"pagegroups": pagegroups,
                   "page": page,
                   "heading": heading,
                   "title": title,
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
            return redirect('waktu')

        return render(request, "jadwal/add_data.html", context)
    else:
        return render(request, "403.html", {} )

def hapus_waktu(request, idWaktu):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka" :
        datanya = get_object_or_404(Waktu, pk=idWaktu)
        try:
            datanya.delete()
            messages.success(request,"Data telah dihapus")
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))
        return redirect("waktu")
    else:
        return render(request, "403.html", {} )

#-------------------------jadwal tampil per kelas------------------------
def kelas(request):
    if "thn_ajaran" in request.POST and request.POST['thn_ajaran'] !="0":
        thnajaran_id=request.POST['thn_ajaran']
    else:
        thnajaran_id=ThnAjaran.objects.latest('id').id
    datanya = Kelas.objects.all().filter(tahun_ajaran = thnajaran_id )
    thnajaran = ThnAjaran.objects.all()
    pagegroups = "jadwalkbm"
    page = "jadwal"
    tahun = "Tahun Ajaran "+ThnAjaran.objects.get(id=thnajaran_id).tahun_ajaran
    breadcrumb = "<li><a href=/home/>Home</a></li><li class=active>Data Jadwal Kelas</li>"
    heading = "Data Jadwal Kelas"
    title = "Data Jadwal Kelas | "

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
                "thnajaran_id": thnajaran_id,
               "linkubah": linkubah,
               "linkhapus": linkhapus,
               }

    return render(request, "jadwal/data_kelas.html",context )

#-------------------------- tampilan jadwal pada kelas-------------------
def jadwal(request, idKelas):
    if request.session['hak_akses'] !="siswa":
        # inisialisasi jadwal kelas
        waktunya = Waktu.objects.all()
        kelass= Kelas.objects.get(id=idKelas)
        cek_jam = Jadwal.objects.filter(kelas=kelass, tahun_ajaran=kelass.tahun_ajaran)
        if not cek_jam.exists():
            for waktu in waktunya:
                Jadwal.objects.get_or_create(waktu=waktu, kelas=kelass, tahun_ajaran=kelass.tahun_ajaran)
        #####################################
        datanya = Jadwal.objects.all().filter(kelas=idKelas).order_by('waktu')
        pagegroups = "jadwalkbm"
        page = "jadwal"
        tahun = ThnAjaran.objects.get(kelas_thnajaran=idKelas).tahun_ajaran
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/jadwal/kelas/>Data Jadwal Kelas</a></li>\
                      <li class=active>Jadwal KBM Kelas "+kelass.nama_kelas+"</li>"
        heading = "Jadwal KBM Kelas <font color=#00ff00><i>"\
                  +kelass.nama_kelas+"</i></font> Tahun Ajaran <font color=#00ff00><i>"\
                  +tahun+"</i></font>"
        title = "Jadwal KBM Kelas | "

        linkhapus = "hapus/"
        mapelnya = MapelDiampu.objects.filter(jadwal_mapeldiampu__kelas__id=idKelas).distinct()
        mapels = mapelnya.count()
        context = {"datanya": datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "linkhapus": linkhapus,
                   "mapels": mapels,
                   "mapelnya": mapelnya,
                   }

        return render(request, "jadwal/jadwal_kelas.html",context )
    else:
        return render(request, "403.html", {} )

def jadwal_all(request, idThn):
    if request.session['hak_akses'] !="siswa":
        datanya = Jadwal.objects.filter(tahun_ajaran=idThn).order_by('waktu')
        pagegroups = "jadwalkbm"
        page = "jadwal"
        tahun = ThnAjaran.objects.get(id=idThn).tahun_ajaran
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/jadwal/kelas/>Data Jadwal Kelas</a></li>\
                      <li class=active>Jadwal KBM Tahun Ajaran"+tahun+"</li>"
        heading = "Jadwal KBM Tahun Ajaran <font color=#00ff00><i>"\
                  +tahun+"</i></font>"
        title = "Jadwal KBM Tahun Ajaran "+tahun+" | "

        linkhapus = "hapus/"


        context = {"datanya": datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "linkhapus": linkhapus,

                   }
        return render(request, "jadwal/data_jadwal.html",context )
    else:
        return render(request, "403.html", {} )

def ubah_jadwal(request, idJadwal):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka":
        datanya = get_object_or_404(Jadwal, pk=idJadwal)
        heading = "Tambah Jadwal KBM"
        title = "Tambah Jadwal KBM | "
        get_jurusan = Kelas.objects.get(jadwal_kelas__id =idJadwal).jurusan
        form = JadwalForm(request.POST or None, request.FILES or None, instance=datanya)
        form.fields['mapel'].queryset = MapelDiampu.objects.filter(Q(mapel__jurusan=get_jurusan) | Q(mapel__jurusan = None))
        context = {"heading": heading,
                   "title": title,
                   "form": form,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                messages.success(request,"Data telah ditambahkan")
                if "done" in request.GET:
                    rendernya = "onload=refreshAndClose()"
                    context={"rendernya": rendernya,}
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal diubah. (%s)' %(err))
        return render(request, "jadwal/popup_add_jadwal.html", context)
    else:
        return render(request, "403.html", {} )


"""
def tambah_jadwal(request, idKelas):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka" :
        thn = ThnAjaran.objects.get(kelas_thnajaran=idKelas)
        kls = Kelas.objects.get(id=idKelas)
        pagegroups = "jadwalkbm"
        page = "jadwal"
        heading = "Tambah Jadwal KBM"
        title = "Tambah Jadwal KBM | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/jadwal/kelas>Data Jadwal Kelas</a></li>\
                      <li><a href=/jadwal/kelas/%s>Jadwal KBM Kelas %s</a></li>\
                      <li class=active>Tambah Jadwal KBM</li>" %(idKelas, kls.nama_kelas)
        linkback = "self.history.back()"

        form = JadwalForm(request.POST or None, request.FILES or None, initial={"kelas": kls, "tahun_ajaran":thn})
        context = {"pagegroups": pagegroups,
                   "page": page,
                   "heading": heading,
                   "title": title,
                   "form": form,
                   "breadcrumb": breadcrumb,
                   "linkback": linkback,

                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                messages.success(request,"Data telah ditambahkan")
            except BaseException, err:
                messages.error(request,err)
            return redirect('/jadwal/kelas/%s' %(idKelas) )

        return render(request, "jadwal/add_data.html", context)
    else:
        return render(request, "403.html", {} )
"""
def hapus_jadwal(request, idJadwal):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka":
        datanya = get_object_or_404(Jadwal, pk=idJadwal)
        idKelas = Jadwal.objects.get(pk=idJadwal).kelas_id
        try:
            datanya.mapel = None
            datanya.ruang = None
            datanya.save()
            messages.success(request,"Data telah dihapus")
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))
        return redirect("/jadwal/kelas/%s" %(idKelas))
    else:
        return render(request, "403.html", {} )

def myjadwal(request):
    if request.session['hak_akses'] =="siswa":
        thnajaran_id=Periode.objects.get(aktif=1).tahun_ajaran.id
        try:
            kelasku = Kelas.objects.get(siswa=request.session['id_user'], tahun_ajaran=thnajaran_id)
        except:
            return render(request, "404.html", {} )
        datanya = Jadwal.objects.all().filter(kelas=kelasku ).order_by('waktu')
        sen = Ruang.objects.filter(jadwal_ruang__waktu__hari__iexact="senin", jadwal_ruang__tahun_ajaran=thnajaran_id,\
                                   jadwal_ruang__kelas=kelasku).distinct()
        sel = Ruang.objects.filter(jadwal_ruang__waktu__hari__iexact="selasa", jadwal_ruang__tahun_ajaran=thnajaran_id,\
                                   jadwal_ruang__kelas=kelasku).distinct()
        rab = Ruang.objects.filter(jadwal_ruang__waktu__hari__iexact="rabu", jadwal_ruang__tahun_ajaran=thnajaran_id,\
                                   jadwal_ruang__kelas=kelasku).distinct()
        kam = Ruang.objects.filter(jadwal_ruang__waktu__hari__iexact="kamis", jadwal_ruang__tahun_ajaran=thnajaran_id,\
                                   jadwal_ruang__kelas=kelasku).distinct()
        jum = Ruang.objects.filter(jadwal_ruang__waktu__hari__iexact="jumat", jadwal_ruang__tahun_ajaran=thnajaran_id,\
                                   jadwal_ruang__kelas=kelasku).distinct()
        sab = Ruang.objects.filter(jadwal_ruang__waktu__hari__iexact="sabtu", jadwal_ruang__tahun_ajaran=thnajaran_id,\
                                   jadwal_ruang__kelas=kelasku).distinct()
        pagegroups = "jadwalkbm"
        page = "jadwalku"

        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li class=active>Jadwal Saya</li>"
        heading = "Jadwal KBM Kelas <font color=#00ff00><i>\
                  %s</i></font> Tahun Ajaran <font color=#00ff00><i>\
                  %s</i></font>" %(kelasku.nama_kelas, kelasku.tahun_ajaran.tahun_ajaran)
        title = "Jadwal Saya | "

        context = {"datanya": datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "sen":sen,
                   "sel":sel,
                   "rab":rab,
                   "kam":kam,
                   "jum":jum,
                   "sab":sab,
                   }
        return render(request, "jadwal/myjadwal_siswa.html",context )
    elif request.session['hak_akses'] =="guru":
        thnajaran_id=Periode.objects.get(aktif=1).tahun_ajaran.id
        try:
            datanya = Jadwal.objects.all().filter(mapel__pengajar=request.session['id_user'], tahun_ajaran=thnajaran_id)
        except:
            return render(request, "404.html", {} )
        pagegroups = "jadwalkbm"
        page = "jadwalku"
        tahun = ThnAjaran.objects.get(id=thnajaran_id).tahun_ajaran
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li class=active>Jadwal Saya</li>"
        heading = "Jadwal KBM<font color=#00ff00><i>\
                  </i></font> Tahun Ajaran <font color=#00ff00><i>"\
                  +tahun+"</i></font>"
        title = "Jadwal Saya | "
        context = {"datanya": datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   }

        return render(request, "jadwal/myjadwal_guru.html",context )
    else:
        return render(request, "403.html", {} )


def cetak_myjadwal(request):
    if request.session['hak_akses'] =="siswa":
        thnajaran_id=Periode.objects.get(aktif=1).tahun_ajaran.id
        try:
            kelasku = Kelas.objects.get(siswa=request.session['id_user'], tahun_ajaran=thnajaran_id)
        except:
            kelasku = Kelas.objects.filter(siswa=request.session['id_user']).latest('id')
        datanya = Jadwal.objects.all().filter(kelas=kelasku ).order_by('waktu')
        pagegroups = "jadwalkbm"
        page = "jadwalku"
        try:
            kelasnya= Kelas.objects.get(id=kelasku.id)
        except:
            return render(request, "404.html", {} )
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li class=active>Jadwal Saya</li>"
        title = "Jadwal Saya | "
        sen = Ruang.objects.filter(jadwal_ruang__waktu__hari__iexact="senin", jadwal_ruang__tahun_ajaran=thnajaran_id).distinct()
        sel = Ruang.objects.filter(jadwal_ruang__waktu__hari__iexact="selasa", jadwal_ruang__tahun_ajaran=thnajaran_id).distinct()
        rab = Ruang.objects.filter(jadwal_ruang__waktu__hari__iexact="rabu", jadwal_ruang__tahun_ajaran=thnajaran_id).distinct()
        kam = Ruang.objects.filter(jadwal_ruang__waktu__hari__iexact="kamis", jadwal_ruang__tahun_ajaran=thnajaran_id).distinct()
        jum = Ruang.objects.filter(jadwal_ruang__waktu__hari__iexact="jumat", jadwal_ruang__tahun_ajaran=thnajaran_id).distinct()
        sab = Ruang.objects.filter(jadwal_ruang__waktu__hari__iexact="sabtu", jadwal_ruang__tahun_ajaran=thnajaran_id).distinct()

        context = {"datanya": datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "kelasnya": kelasnya,
                   "title": title,
                   "sen":sen,
                   "sel":sel,
                   "rab":rab,
                   "kam":kam,
                   "jum":jum,
                   "sab":sab,
                   }
        return render(request, "jadwal/cetak_myjadwal_siswa.html",context )
    elif request.session['hak_akses'] =="guru":
        thnajaran_id=ThnAjaran.objects.latest('id').id
        datanya = Jadwal.objects.all().filter(mapel__pengajar=request.session['id_user'], tahun_ajaran=thnajaran_id).order_by('waktu')
        tahun = ThnAjaran.objects.get(id=thnajaran_id).tahun_ajaran
        jumlah_jam = datanya.count()
        tanggal = datetime.now().date()
        kepala = Guru.objects.get(jabatan__nama_jabatan="Kepala Sekolah")
        title = "Jadwal Saya | "
        context = {"datanya": datanya,
                   "title": title,
                   "tahun": tahun,
                   "jumlah_jam": jumlah_jam,
                   "tanggal": tanggal,
                   "kepala": kepala,
                   }

        return render(request, "jadwal/cetak_myjadwal_guru.html",context )
    else:
        return render(request, "403.html", {} )
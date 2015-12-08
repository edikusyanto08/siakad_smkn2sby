from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from jadwal.models import Jadwal
from django.contrib import messages
from decimal import Decimal

# Create your views here

def periode(request):
    if request.session['hak_akses'] !="siswa" or request.session['hak_akses'] != "guru":
        page = "periode"
        pagegroups = "penilaian"
        breadcrumb = "<li><a href=/home/>Home</a></li><li class=active>Data Periode</li>"
        heading = "Data Periode"
        title = heading+" | "
        datanya = Periode.objects.all()
        try:
            Periode.objects.get(aktif=1)
        except:
            p = Periode.objects.latest('id')
            p.aktif = 1
            p.save()
        context = {"pagegroups": pagegroups,
                    "page": page,
                    "datanya": datanya,
                    "breadcrumb": breadcrumb,
                    "heading": heading,
                    "title": title,
                    }
        return render(request, "penilaian/data_periode.html",context )
    else:
        return render(request, "403.html", {} )

def tambah_periode(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka":
        page = "periode"
        pagegroups = "penilaian"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/penilaian/periode>Data Periode</a></li>\
                      <li class=active>Tambah Data Periode</li>"
        heading = "Tambah Data Periode"
        title = heading+" | "
        form = PeriodeForm(request.POST or None, request.FILES or None)
        context = {"pagegroups": pagegroups,
                    "page": page,
                    "form": form,
                    "breadcrumb": breadcrumb,
                    "heading": heading,
                    "title": title,
                    }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                messages.success(request,"Data telah ditambahkan")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
            return redirect('periode')
        return render(request, "penilaian/add_data.html",context )
    else:
        return render(request, "403.html", {} )

def aktif_periode(request, idPeriode):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka":
        datanya = get_object_or_404(Periode, pk=idPeriode)
        if datanya.aktif == 0 :
            datanya.aktif = 1
            datanya.save()
            messages.success(request,"Periode diaktifkan")
        else:
            datanya.aktif = 0
            datanya.save()
            cek = Periode.objects.filter(aktif=1)
            if not cek.exists():
                datanya.aktif = 1
                datanya.save()
                messages.error(request,"Minimal ada satu periode aktif.")
            else:
                messages.warning(request,"Periode di non-aktifkan. Semua data penilaian yang \
                                    berhubungan dengan periode dipilih akan di non-aktifkan.")
        periodes = Periode.objects.all().exclude(id=datanya.id)
        for periode in periodes:
            if datanya.aktif == 1 :
                periode.aktif = 0
                periode.save()
        return redirect("periode")
    else:
        return render(request, "403.html", {} )

def verifikasi(request, idPeriode):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka":
        datanya = get_object_or_404(Periode, pk=idPeriode)
        if datanya.verifikasi == 0 :
            datanya.verifikasi = 1
            datanya.save()
            messages.success(request,"Periode %s %s telah diverifikasi. Semua penilaian pada periode ini akan di non-aktifkan." %(datanya.semester, datanya.tahun_ajaran))
        else:
            datanya.verifikasi = 0
            datanya.save()
            messages.warning(request,"Verifikasi %s %s dibatalkan. Semua penilaian pada periode ini diaktifkan. "  %(datanya.semester, datanya.tahun_ajaran))
        return redirect("periode")
    else:
        return render(request, "403.html", {} )

def ubah_periode(request, idPeriode):
    datanya = Periode.objects.get(id=idPeriode)
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka":
        page = "periode"
        pagegroups = "penilaian"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                      <li><a href=/penilaian/periode>Data Periode</a></li>\
                      <li class=active>Ubah Data Periode</li>"
        heading = "Ubah Data Periode"
        title = heading+" | "
        form = PeriodeForm(request.POST or None, request.FILES or None, instance=datanya)
        context = {"pagegroups": pagegroups,
                    "page": page,
                    "form": form,
                    "breadcrumb": breadcrumb,
                    "heading": heading,
                    "title": title,
                    }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                messages.success(request,"Data berhasil diubah")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal diubah. (%s)' %(err))
            return redirect('periode')
        return render(request, "penilaian/add_data.html",context )
    else:
        return render(request, "403.html", {} )

def hapus_periode(request, idPeriode):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="waka":
        datanya = get_object_or_404(Periode, pk=idPeriode)
        if Periode.objects.count() > 1:
            try:
                datanya.delete()
                messages.success(request,"Data telah dihapus")
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))
        else:
            messages.error(request,"Minimal harus ada periode.")
        return redirect('periode')
    else:
        return render(request, "403.html", {} )

def rekap_pilih_mapel(request):#view rekap memilih mapel diampu dan kelas
    if request.session['hak_akses'] =="guru":
        if "mapel_id" in request.POST:
            mapel_id=request.POST['mapel_id']
        else:
            try:
                del request.session['mapel_id']
                del request.session['kelas_id']
            except: pass
            mapel_id=0
        if "kelas_id" in request.POST:
            request.session['kelas_id'] = request.POST['kelas_id']
            return redirect("rekap_siswa")
        request.session['mapel_id'] = mapel_id
        periode = Periode.objects.get(aktif=1)
        periodes = Periode.objects.filter(aktif=1)
        thn = ThnAjaran.objects.get(periode_tahun=periode)
        datanya = Kelas.objects.filter(jadwal_kelas__mapel__pengajar=request.session['id_user'],\
                                       jadwal_kelas__tahun_ajaran=thn,\
                                       jadwal_kelas__mapel__mapel=mapel_id).distinct()
        mapels = Mapel.objects.filter(mapeldiampu_mapel__jadwal_mapeldiampu__tahun_ajaran=thn,\
                                      mapeldiampu_mapel__pengajar=request.session['id_user']).distinct()
        pagegroups = "penilaian"
        page = "rekap_nilai"
        try:
            mapelnya = Mapel.objects.get(id=mapel_id)
            heading = "Data Kelas yang Diampu %s (%s %s)" %(mapelnya.nama_mapel, periode.semester, periode.tahun_ajaran)
        except:
            heading = "Pilih Mapel Yang Diampu"
        breadcrumb = "<li><a href=/home/>Home</a></li><li class=active>Pilih Mapel dan Kelas</li>"
        title = heading+" | "
        context = {"datanya": datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "mapels": mapels,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "mapel_id": mapel_id,
                   "periodes": periodes,
                   }

        return render(request, "penilaian/data_kelas.html",context )
    else:
        return render(request, "403.html", {} )

def rekap_pilih_siswa(request):#----------view rekap setelah memilih mapel dan kelas
    if request.session['hak_akses'] =="guru":
        try:
            kelas = Kelas.objects.get(id=request.session['kelas_id'])
            mapel = Mapel.objects.get(id=request.session['mapel_id'])
            periode = Periode.objects.get(aktif=1)
            pengajar = Guru.objects.get(id=request.session['id_user'])
        except:
            return redirect("rekap_pilih_mapel")
        datanya = Siswa.objects.filter(kelas_siswa__kelas__id=request.session['kelas_id'])
        #inisialisasi nilai sikap, keterampilan dan kognitif
        for siswa in datanya:
            try:
                nilainya, created = NilaiSikap.objects.get_or_create(siswa=siswa, kelas=kelas, mapel=mapel, periode=periode, pengajar=pengajar)
                NilaiKeterampilan.objects.get_or_create(siswa=siswa, kelas=kelas, mapel=mapel, periode=periode, pengajar=pengajar)
                NilaiKognitif.objects.get_or_create(siswa=siswa, kelas=kelas, mapel=mapel, periode=periode, pengajar=pengajar)
                NilaiTotal.objects.get_or_create(siswa=siswa, kelas=kelas, mapel=mapel, periode=periode, pengajar=pengajar)
                hitung_total(nilainya.siswa, nilainya.kelas, nilainya.mapel, nilainya.periode, nilainya.pengajar)
            except BaseException, err:
                messages.error(request, "Terjadi kesalahan, %s" %(err))
        nilaisikap = NilaiSikap.objects.filter(kelas=kelas, periode=periode, mapel=mapel)
        nilaiketerampilan = NilaiKeterampilan.objects.filter(kelas=kelas, periode=periode, mapel=mapel)
        nilaikognitif = NilaiKognitif.objects.filter(kelas=kelas, periode=periode, mapel=mapel)
        nilaitotal = NilaiTotal.objects.filter(kelas=kelas, periode=periode, mapel=mapel)
        pagegroups = "penilaian"
        page = "rekap_nilai"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                            <li><a href=/penilaian/rekap/>Pilih Mapel dan Kelas</a></li>\
                            <li class=active>Nilai Siswa kelas %s %s</li>" %(mapel.nama_mapel, kelas.nama_kelas)
        heading = "Nilai Siswa Kelas %s %s Periode %s %s" %(mapel.nama_mapel, kelas.nama_kelas, periode.semester, periode.tahun_ajaran)
        title = heading+" | "
        pengampu = Guru.objects.filter(mapeldiampu_guru__jadwal_mapeldiampu__kelas=kelas, mapeldiampu_guru__mapel=mapel).distinct()
        context = {
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "nilaisikap": nilaisikap,
                   "nilaiketerampilan": nilaiketerampilan,
                   "nilaikognitif": nilaikognitif,
                   "nilaitotal": nilaitotal,
                   "periode": periode,
                   "pengampu": pengampu,
                   }

        return render(request, "penilaian/data_siswa.html",context )
    else:
        return render(request, "403.html", {} )

def popup_sikap(request, idNSikap):
    try:
        datanya = get_object_or_404(NilaiSikap, id=idNSikap)
    except:
        return render(request, "404.html", {} )
    if request.session['hak_akses'] =="guru" and datanya.pengajar.id == request.session['id_user'] and datanya.periode.aktif and not datanya.periode.verifikasi:
        heading = "Input Nilai Sikap Siswa %s " %(datanya.siswa.nama_lengkap)
        title = heading+" | "
        form = EntryNilaiSikapForm(request.POST or None, request.FILES or None, instance=datanya)
        context = {"datanya": datanya,
                   "heading": heading,
                   "title": title,
                   "form": form,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            save_it.save()
            nilainya = get_object_or_404(NilaiSikap, id=idNSikap)
            try:
                observasi = Decimal(form.cleaned_data.get('observasi'))
                nilai_diri = Decimal(form.cleaned_data.get('penilaian_diri'))
                nilai_sejawat = Decimal(form.cleaned_data.get('penilaian_sejawat'))
                jurnal = Decimal(form.cleaned_data.get('jurnal'))
                rerata = (observasi+nilai_diri+nilai_sejawat+jurnal)/Decimal(4)
                konversi = rerata/Decimal(0.25)/Decimal(100)
                predikat = hitung_predikat(konversi)
                nilainya.rerata=rerata
                nilainya.konversi=konversi
                nilainya.predikat=predikat
                nilainya.save()
                aa = hitung_total(nilainya.siswa, nilainya.kelas, nilainya.mapel, nilainya.periode, nilainya.pengajar)
                messages.success(request,"Nilai berhasil diubah %s" %(aa))
                if "done" in request.GET:
                    rendernya = "onload=refreshAndClose()"
                    context={"rendernya": rendernya,}
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Nilai gagal diubah. (%s)' %(err))
        return render(request, "penilaian/popupentry.html", context)
    else:
        return render(request, "403.html", {} )

def popup_keterampilan(request, idNKeterampilan):
    try:
        datanya = get_object_or_404(NilaiKeterampilan, id=idNKeterampilan)
    except:
        return render(request, "404.html", {} )
    if request.session['hak_akses'] =="guru" and datanya.pengajar.id == request.session['id_user'] and datanya.periode.aktif and not datanya.periode.verifikasi:
        heading = "Input Nilai Keterampilan Siswa %s " %(datanya.siswa.nama_lengkap)
        title = heading+" | "
        form = EntryNilaiKeterampilanForm(request.POST or None, request.FILES or None, instance=datanya)
        context = {"datanya": datanya,
                   "heading": heading,
                   "title": title,
                   "form": form,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            save_it.save()
            nilainya = get_object_or_404(NilaiKeterampilan, id=idNKeterampilan)
            try:
                praktik = Decimal(form.cleaned_data.get('praktik'))
                project = Decimal(form.cleaned_data.get('project'))
                portofolio = Decimal(form.cleaned_data.get('portofolio'))
                rerata = (praktik+project+portofolio)/Decimal(3)
                konversi = rerata/Decimal(0.25)/Decimal(100)
                predikat = hitung_predikat(konversi)
                nilainya.rerata=rerata
                nilainya.konversi=konversi
                nilainya.predikat=predikat
                nilainya.save()
                aa = hitung_total(nilainya.siswa, nilainya.kelas, nilainya.mapel, nilainya.periode, nilainya.pengajar)
                messages.success(request,"Nilai berhasil diubah %s" %(aa))
                if "done" in request.GET:
                    rendernya = "onload=refreshAndClose()"
                    context={"rendernya": rendernya,}
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Nilai gagal diubah. (%s)' %(err))
        return render(request, "penilaian/popupentry.html", context)
    else:
        return render(request, "403.html", {} )

def popup_un(request, idNun):
    try:
        datanya = get_object_or_404(NilaiUN, id=idNun)
    except:
        return render(request, "404.html", {} )
    if request.session['hak_akses'] == "staf" :
        heading = "Input Nilai Ujian Nasional Siswa %s " %(datanya.siswa.nama_lengkap)
        title = heading+" | "
        form = EntryNilaiUNForm(request.POST or None, request.FILES or None, instance=datanya)
        context = {"datanya": datanya,
                   "heading": heading,
                   "title": title,
                   "form": form,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            save_it.save()
            nilainya = get_object_or_404(NilaiUN, id=idNun)
            try:
                nilai = Decimal(form.cleaned_data.get('nilai'))
                konversi = nilai/Decimal(0.25)/Decimal(100)
                predikat = hitung_predikat(konversi)
                nilainya.konversi=konversi
                nilainya.predikat=predikat
                nilainya.save()
                messages.success(request,"Nilai berhasil diubah")
                if "done" in request.GET:
                    rendernya = "onload=refreshAndClose()"
                    context={"rendernya": rendernya,}
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Nilai gagal diubah. (%s)' %(err))
        return render(request, "penilaian/popupentry.html", context)
    else:
        return render(request, "403.html", {} )

def popup_us(request, idNus):
    try:
        datanya = get_object_or_404(NilaiUS, id=idNus)
    except:
        return render(request, "404.html", {} )
    if request.session['hak_akses'] == "staf" :
        heading = "Input Nilai Ujian Sekolah Siswa %s " %(datanya.siswa.nama_lengkap)
        title = heading+" | "
        form = EntryNilaiUSForm(request.POST or None, request.FILES or None, instance=datanya)
        context = {"datanya": datanya,
                   "heading": heading,
                   "title": title,
                   "form": form,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            save_it.save()
            nilainya = get_object_or_404(NilaiUS, id=idNus)
            try:
                nilai = Decimal(form.cleaned_data.get('nilai'))
                konversi = nilai/Decimal(0.25)/Decimal(100)
                predikat = hitung_predikat(konversi)
                nilainya.konversi=konversi
                nilainya.predikat=predikat
                nilainya.save()
                messages.success(request,"Nilai berhasil diubah")
                if "done" in request.GET:
                    rendernya = "onload=refreshAndClose()"
                    context={"rendernya": rendernya,}
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Nilai gagal diubah. (%s)' %(err))
        return render(request, "penilaian/popupentry.html", context)
    else:
        return render(request, "403.html", {} )

def popup_kognitif(request, idNKognitif):
    try:
        datanya = get_object_or_404(NilaiKognitif, id=idNKognitif)
    except:
        return render(request, "404.html", {} )
    if request.session['hak_akses'] =="guru" and datanya.pengajar.id == request.session['id_user'] and datanya.periode.aktif and not datanya.periode.verifikasi:
        heading = "Input Nilai Keterampilan Siswa %s " %(datanya.siswa.nama_lengkap)
        title = heading+" | "
        form = EntryNilaiKognitifForm(request.POST or None, request.FILES or None, instance=datanya)
        context = {"datanya": datanya,
                   "heading": heading,
                   "title": title,
                   "form": form,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            save_it.save()
            nilainya = get_object_or_404(NilaiKognitif, id=idNKognitif)
            try:
                tugas = Decimal(form.cleaned_data.get('tugas'))
                uh = Decimal(form.cleaned_data.get('uh'))
                uts = Decimal(form.cleaned_data.get('uts'))
                uas = Decimal(form.cleaned_data.get('uas'))
                tugas_uh = (tugas+uh)/Decimal(2)
                rerata = (tugas_uh+uts+uas)/Decimal(3)
                konversi = rerata/Decimal(0.25)/Decimal(100)
                predikat = hitung_predikat(konversi)
                nilainya.rerata=rerata
                nilainya.konversi=konversi
                nilainya.predikat=predikat
                nilainya.save()
                aa = hitung_total(nilainya.siswa, nilainya.kelas, nilainya.mapel, nilainya.periode, nilainya.pengajar)
                messages.success(request,"Nilai berhasil diubah %s" %(aa))
                if "done" in request.GET:
                    rendernya = "onload=refreshAndClose()"
                    context={"rendernya": rendernya,}
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Nilai gagal diubah. (%s)' %(err))
        return render(request, "penilaian/popupentry.html", context)
    else:
        return render(request, "403.html", {} )

def popup_kompetensi(request, idNKompetensi):
    try:
        datanya = get_object_or_404(NilaiKompetensi, id=idNKompetensi)
    except:
        return render(request, "404.html", {} )
    if request.session['hak_akses'] =="guru" and datanya.pengajar.id == request.session['id_user'] and datanya.periode.aktif and not datanya.periode.verifikasi:
        heading = "Input Nilai Kompetensi Siswa %s " %(datanya.siswa.nama_lengkap)
        title = heading+" | "
        form = EntryNilaiKompetensiForm(request.POST or None, request.FILES or None, instance=datanya)
        context = {"datanya": datanya,
                   "heading": heading,
                   "title": title,
                   "form": form,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            save_it.save()
            nilainya = get_object_or_404(NilaiKompetensi, id=idNKompetensi)
            try:
                nilai = Decimal(form.cleaned_data.get('nilai'))
                konversi = nilai/Decimal(0.25)/Decimal(100)
                predikat = hitung_predikat(konversi)
                nilainya.konversi=konversi
                nilainya.predikat=predikat
                nilainya.save()
                messages.success(request,"Nilai berhasil diubah")
                if "done" in request.GET:
                    rendernya = "onload=refreshAndClose()"
                    context={"rendernya": rendernya,}
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Nilai gagal diubah. (%s)' %(err))
        return render(request, "penilaian/popupentry.html", context)
    else:
        return render(request, "403.html", {} )

def hitung_predikat(konversii):
    konversi = float(konversii)
    if konversi >= 3.85 and konversi <= 4.00 :
        predikat = "A"
    elif konversi >= 3.51 and konversi <= 3.84 :
        predikat = "A-"
    elif konversi >= 3.18 and konversi <= 3.50 :
        predikat = "B+"
    elif konversi >= 2.85 and konversi <= 3.17 :
        predikat = "B"
    elif konversi >= 2.51 and konversi <= 2.84 :
        predikat = "B-"
    elif konversi >= 2.18 and konversi <= 2.50 :
        predikat = "C+"
    elif konversi >= 1.85 and konversi <= 2.17 :
        predikat ="C"
    elif konversi >= 1.51 and konversi <= 1.84 :
        predikat = "C-"
    elif konversi >= 1.18 and konversi <= 1.50 :
        predikat = "D+"
    elif konversi >= 0.00 and konversi <= 1.17 :
        predikat = "D"
    return predikat

def hitung_total(siswa, kelas, mapel, periode, pengajar):
    try:
        nilai_sikap = NilaiSikap.objects.get(siswa=siswa, kelas=kelas, mapel=mapel, periode=periode, pengajar=pengajar)
        nilai_keterampilan = NilaiKeterampilan.objects.get(siswa=siswa, kelas=kelas, mapel=mapel, periode=periode, pengajar=pengajar)
        nilai_kognitif = NilaiKognitif.objects.get(siswa=siswa, kelas=kelas, mapel=mapel, periode=periode, pengajar=pengajar)
        nilai_total = NilaiTotal.objects.get(siswa=siswa, kelas=kelas, mapel=mapel, periode=periode, pengajar=pengajar)
        nilai_total.nilai_sikap = nilai_sikap.rerata
        nilai_total.nilai_sikap_konv = nilai_sikap.konversi
        nilai_total.nilai_sikap_pre = nilai_sikap.predikat
        #nilai_total.save()
        nilai_total.nilai_keterampilan = nilai_keterampilan.rerata
        nilai_total.nilai_keterampilan_konv = nilai_keterampilan.konversi
        nilai_total.nilai_keterampilan_pre = nilai_keterampilan.predikat
        #nilai_total.save()
        nilai_total.nilai_kognitif = nilai_kognitif.rerata
        nilai_total.nilai_kognitif_konv = nilai_kognitif.konversi
        nilai_total.nilai_kognitif_pre = nilai_kognitif.predikat
        #nilai_total.save()
        nilai_total.rerata = (Decimal(nilai_sikap.rerata)+Decimal(nilai_keterampilan.rerata)+Decimal(nilai_kognitif.rerata))/Decimal(3)
        nilai_total.konversi = nilai_total.rerata/Decimal(0.25)/Decimal(100)
        nilai_total.predikat = hitung_predikat(nilai_total.konversi)
        if nilai_total.konversi < Decimal(periode.kkm):
            nilai_total.keterangan = "Belum Tuntas"
        else:
            nilai_total.keterangan = "Tuntas"
        nilai_total.save()
        pesan = ""
    except BaseException, err:
        pesan = err
    return pesan

def nilai_kelas(request):#memilih kelas untuk meilhat nilai
    if request.session['hak_akses'] !="guru" and request.session['hak_akses'] !="siswa":
        if "periode_id" in request.POST:
            periode_id = request.POST['periode_id']
        else:
            try:
                del request.session['mapel_id']
                del request.session['kelas_id']
                del request.session['periode_id']
            except: pass
            periode_id = Periode.objects.latest('id').id
        if "kelas_id" in request.POST:
            request.session['kelas_id'] = request.POST['kelas_id']
            return redirect("nilai_siswa")
        request.session['periode_id'] = periode_id
        periode=Periode.objects.get(id=periode_id)
        periodes=Periode.objects.all()
        thn = ThnAjaran.objects.get(periode_tahun=periode)
        datanya = Kelas.objects.filter(tahun_ajaran=thn)
        pagegroups = "penilaian"
        page = "data_nilai"
        breadcrumb = "<li><a href=/home/>Home</a></li><li class=active>Pilih Mapel dan Kelas</li>"
        heading = "Data Kelas (%s %s)" %(periode.semester, periode.tahun_ajaran)
        title = heading+" | "
        context = {"datanya": datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "periodes": periodes,
                   "periode_id": periode_id,
                   }

        return render(request, "penilaian/data_kelas.html",context )
    else:
        return render(request, "403.html", {} )

def nilai_siswa(request):
    if request.session['hak_akses'] !="guru" and request.session['hak_akses'] !="siswa":
        try:
            kelas = Kelas.objects.get(id=request.session['kelas_id'])
            periode = Periode.objects.get(id=request.session['periode_id'])
        except:
            return redirect("nilai_kelas")
        pagegroups = "penilaian"
        page = "data_nilai"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                            <li><a href=/penilaian/nilai/>Pilih Mapel dan Kelas</a></li>\
                            <li class=active>Nilai Siswa kelas%s</li>" %(kelas.nama_kelas)
        heading = "Nilai Siswa Kelas %s Periode %s %s" %(kelas.nama_kelas, periode.semester, periode.tahun_ajaran)
        title = heading+" | "
        siswas = Siswa.objects.filter(kelas_siswa__kelas__id=kelas.id)
        mapels = Mapel.objects.filter(mapeldiampu_mapel__jadwal_mapeldiampu__kelas__id=kelas.id).distinct()
        nilais = NilaiTotal.objects.filter(kelas__id=kelas.id, periode=periode)
        context = {
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "siswas": siswas,
                    "mapels": mapels,
                    "nilais": nilais,
                    "periode": periode,
                   }
        return render(request, "penilaian/nilai_siswa.html",context )
    else:
        return render(request, "403.html", {} )

def detil_mapel(request, idMapel):#halaman jika kode mapel diklik
   if request.session['hak_akses'] !="guru" and request.session['hak_akses'] !="siswa":
        try:
            kelas = Kelas.objects.get(id=request.session['kelas_id'])
            mapel = Mapel.objects.get(id=idMapel)
            periode = Periode.objects.get(id=request.session['periode_id'])
        except:
            return redirect("nilai_kelas")
        nilaisikap = NilaiSikap.objects.filter(kelas=kelas, periode=periode, mapel=mapel)
        nilaiketerampilan = NilaiKeterampilan.objects.filter(kelas=kelas, periode=periode, mapel=mapel)
        nilaikognitif = NilaiKognitif.objects.filter(kelas=kelas, periode=periode, mapel=mapel)
        nilaitotal = NilaiTotal.objects.filter(kelas=kelas, periode=periode, mapel=mapel)
        pagegroups = "penilaian"
        page = "data_nilai"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                            <li><a href=/penilaian/nilai/>Pilih Mapel dan Kelas</a></li>\
                            <li class=active>Nilai Siswa kelas %s %s</li>" %(mapel.nama_mapel, kelas.nama_kelas)
        heading = "Nilai Siswa Kelas %s %s Periode %s %s" %(mapel.nama_mapel, kelas.nama_kelas, periode.semester, periode.tahun_ajaran)
        title = heading+" | "
        pengampu = Guru.objects.filter(mapeldiampu_guru__jadwal_mapeldiampu__kelas=kelas, mapeldiampu_guru__mapel=mapel).distinct()
        context = {
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "nilaisikap": nilaisikap,
                   "nilaiketerampilan": nilaiketerampilan,
                   "nilaikognitif": nilaikognitif,
                   "nilaitotal": nilaitotal,
                   "pengampu": pengampu,
                   "periode": periode,
                   }

        return render(request, "penilaian/data_siswa.html",context )
   else:
        return render(request, "403.html", {} )

def rekapkomp_pilih_kelas(request):#memilih kelas pada rekap kompetensi kejuruan
    if request.session['hak_akses'] == "guru":
        if "mapel_id" in request.POST:
            mapel_id=request.POST['mapel_id']
        else:
            try:
                del request.session['mapel_id']
                del request.session['kelas_id']
            except: pass
            mapel_id=0
        if "kelas_id" in request.POST:
            request.session['kelas_id'] = request.POST['kelas_id']
            return redirect(rekapkomp_pilih_siswa)
        request.session['mapel_id'] = mapel_id
        periode=Periode.objects.get(aktif=1)
        periodes=Periode.objects.filter(aktif=1)
        thn = ThnAjaran.objects.get(periode_tahun=periode)
        datanya = Kelas.objects.filter(jadwal_kelas__mapel__pengajar=request.session['id_user'],\
                                       jadwal_kelas__tahun_ajaran=thn,\
                                       jadwal_kelas__mapel__mapel=mapel_id).distinct()
        mapels = Mapel.objects.filter(mapeldiampu_mapel__jadwal_mapeldiampu__tahun_ajaran=thn,\
                                      mapeldiampu_mapel__pengajar=request.session['id_user']).exclude(jurusan=None).distinct()
        pagegroups = "penilaian"
        page = "rekap_komp"
        try:
            mapelnya = Mapel.objects.get(id=mapel_id)
            heading = "Data Kelas yang Diampu %s (%s %s)" %(mapelnya.nama_mapel, periode.semester, periode.tahun_ajaran)
        except:
            heading = "Pilih Mapel Yang Diampu"
        breadcrumb = "<li><a href=/home/>Home</a></li><li class=active>Pilih Mapel dan Kelas</li>"
        title = heading+" | "
        context = {"datanya": datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "mapels": mapels,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "mapel_id": mapel_id,
                   "periodes": periodes,
                   }

        return render(request, "penilaian/data_kelas.html",context )
    else:
        return render(request, "403.html", {} )

def rekapkomp_pilih_siswa(request):
    if request.session['hak_akses'] =="guru":
        try:
            kelas = Kelas.objects.get(id=request.session['kelas_id'])
            mapel = Mapel.objects.get(id=request.session['mapel_id'])
            periode = Periode.objects.get(aktif=1)
            pengajar = Guru.objects.get(id=request.session['id_user'])
            if not mapel.jurusan:
                return redirect("rekapkomp_pilih_kelas")
        except:
            return redirect("rekapkomp_pilih_kelas")
        datanya = Siswa.objects.filter(kelas_siswa__kelas__id=request.session['kelas_id'])
        kompetensi = KompetensiKejuruan.objects.filter(mapel_induk=mapel)

        for siswa in datanya:
            for komp in kompetensi:
                try:
                    data, created=NilaiKompetensi.objects.get_or_create(siswa=siswa, kelas=kelas, mapel=mapel, kompetensi=komp,\
                                                          pengajar=pengajar)
                    if not data.periode:
                        data.periode=periode
                        data.save()
                except BaseException, err:
                    messages.error(request, "Terjadi kesalahan, %s" %(err))
        pagegroups = "penilaian"
        page = "rekap_komp"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                            <li><a onclick=self.history.back()>Pilih Mapel dan Kelas</a></li>\
                            <li class=active>Pilih Siswa</li>"
        heading = "Data Siswa Kelas %s %s Periode %s %s" %(mapel.nama_mapel, kelas.nama_kelas, periode.semester, periode.tahun_ajaran)
        title = heading+" | "
        context = {
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "periode": periode,
                   "datanya": datanya,
                   }

        return render(request, "penilaian/komp_siswa.html",context )
    else:
        return render(request, "403.html", {} )

def rekapkomp_siswa(request, idSiswa):
    if request.session['hak_akses'] =="guru":
        try:
            mapel = Mapel.objects.get(id=request.session['mapel_id'])
            if not mapel.jurusan:
                return redirect("kompetensi_kelas")
        except:
            return redirect("kompetensi_kelas")
        siswa = Siswa.objects.get(id=idSiswa)
        datanya = NilaiKompetensi.objects.filter(siswa=siswa, mapel=mapel)
        #inisialisasi nilai sikap, keterampilan dan kognitif
        pagegroups = "penilaian"
        page = "rekap_komp"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                            <li><a href=/penilaian/kompetensi/>Pilih Mapel dan Kelas</a></li>\
                            <li><a onclick=self.history.back()>Pilih Siswa</a></li>\
                            <li class=active>Data Kompetensi Siswa</li>"
        heading = "Data Kompetensi Siswa %s %s" %(mapel.nama_mapel, siswa.nama_lengkap)
        title = heading+" | "
        context = {
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "datanya": datanya,
                   }

        return render(request, "penilaian/rekapkomp_list.html",context )
    else:
        return render(request, "403.html", {} )

def rekapun_pilih_kelas(request):#memilih kelas pada rekap nilai un
    if request.session['hak_akses'] !="siswa":
        if "tahun" in request.POST:
            thn = request.POST['tahun']
        else:
            thn = 0
        tahun = ThnAjaran.objects.all()
        if "kelas_id" in request.POST:
            request.session['kelas_id'] = request.POST['kelas_id']
            return redirect("rekapun_pilih_siswa")
        datanya = Kelas.objects.filter(tahun_ajaran=thn, nama_kelas__istartswith="XII")
        pagegroups = "penilaian"
        page = "rekap_un"
        heading = "Pilih Kelas"
        breadcrumb = "<li><a href=/home/>Home</a></li><li class=active>Pilih Kelas</li>"
        title = heading+" | "
        context = {"datanya": datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "tahun": tahun,
                   }
        return render(request, "penilaian/data_kelas.html",context )
    else:
        return render(request, "403.html", {} )

def rekapun_pilih_siswa(request):
    if request.session['hak_akses'] !="siswa":
        try:
            kelas = Kelas.objects.get(id=request.session['kelas_id'])
        except:
            return redirect("rekapkomp_pilih_kelas")
        datanya = Siswa.objects.filter(kelas_siswa__kelas__id=request.session['kelas_id'])
        thn = ThnAjaran.objects.latest('id')
        mapels = MapelUN.objects.all()
        for siswa in datanya:
            for mapel in mapels:
                try:
                    NilaiUN.objects.get_or_create(siswa=siswa, kelas=kelas, mapel=mapel.mapel, tahun_ajaran=thn)
                except BaseException, err:
                    messages.error(request, "Terjadi kesalahan, %s" %(err))
        pagegroups = "penilaian"
        page = "rekap_un"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                            <li><a href=/penilaian/rekap/un/>Pilih Kelas</a></li>\
                            <li class=active>Pilih Siswa</li>"
        heading = "Data Siswa Kelas %s Tahun Ajaran %s" %(kelas.nama_kelas,thn.tahun_ajaran)
        title = heading+" | "
        context = {
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "datanya": datanya,
                   }

        return render(request, "penilaian/komp_siswa.html",context )
    else:
        return render(request, "403.html", {} )

def rekapun_siswa(request, idSiswa):
    if request.session['hak_akses'] !="siswa":
        siswa = Siswa.objects.get(id=idSiswa)
        datanya = NilaiUN.objects.filter(siswa=siswa)

        pagegroups = "penilaian"
        page = "rekap_un"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                            <li><a href=/penilaian/un/>Pilih Kelas</a></li>\
                            <li><a onclick=self.history.back()>Pilih Siswa</a></li>\
                            <li class=active>Data Nilai UN Siswa</li>"
        heading = "Data Nilai Ujian Nasional Siswa %s" %(siswa.nama_lengkap)
        title = heading+" | "
        context = {
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "datanya": datanya,
                   }
        return render(request, "penilaian/rekapun_list.html",context )
    else:
        return render(request, "403.html", {} )

def rekapus_pilih_kelas(request):#memilih kelas pada rekap nilai un
    if request.session['hak_akses'] !="siswa":
        if "tahun" in request.POST:
            thn = request.POST['tahun']
        else:
            thn = 0
        tahun = ThnAjaran.objects.all()
        if "kelas_id" in request.POST:
            request.session['kelas_id'] = request.POST['kelas_id']
            return redirect("rekapus_pilih_siswa")
        datanya = Kelas.objects.filter(tahun_ajaran=thn, nama_kelas__istartswith="XII")
        pagegroups = "penilaian"
        page = "rekap_us"
        heading = "Pilih Kelas"
        breadcrumb = "<li><a href=/home/>Home</a></li><li class=active>Pilih Kelas</li>"
        title = heading+" | "
        context = {"datanya": datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "tahun": tahun,
                   }
        return render(request, "penilaian/data_kelas.html",context )
    else:
        return render(request, "403.html", {} )

def rekapus_pilih_siswa(request):
    if request.session['hak_akses'] !="siswa":
        try:
            kelas = Kelas.objects.get(id=request.session['kelas_id'])
        except:
            return redirect("rekapkomp_pilih_kelas")
        datanya = Siswa.objects.filter(kelas_siswa__kelas__id=request.session['kelas_id'])
        pagegroups = "penilaian"
        page = "rekap_us"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                            <li><a href=/penilaian/rekap/us/>Pilih Kelas</a></li>\
                            <li class=active>Pilih Siswa</li>"
        heading = "Data Siswa Kelas %s Tahun Ajaran %s" %(kelas.nama_kelas, kelas.tahun_ajaran.tahun_ajaran)
        title = heading+" | "
        context = {
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "datanya": datanya,
                   }

        return render(request, "penilaian/komp_siswa.html",context )
    else:
        return render(request, "403.html", {} )

def rekapus_siswa(request, idSiswa):
    if request.session['hak_akses'] !="siswa":
        siswa = Siswa.objects.get(id=idSiswa)
        kelas = Kelas.objects.get(id=request.session["kelas_id"])
        thn = ThnAjaran.objects.latest('id')
        mapels = Mapel.objects.filter(mapeldiampu_mapel__jadwal_mapeldiampu__kelas__kelas_siswa__siswa__id=idSiswa).distinct()
        for mapel in mapels:
            try:
                NilaiUS.objects.get_or_create(siswa=siswa, kelas=kelas, mapel=mapel, tahun_ajaran=thn)
            except BaseException, err:
                messages.error(request, "Terjadi kesalahan, %s" %(err))
        datanya = NilaiUS.objects.filter(siswa=siswa)
        pagegroups = "penilaian"
        page = "rekap_us"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                            <li><a href=/penilaian/us/>Pilih Kelas</a></li>\
                            <li><a onclick=self.history.back()>Pilih Siswa</a></li>\
                            <li class=active>Data Nilai US Siswa</li>"
        heading = "Data Nilai Ujian Sekolah Siswa %s" %(siswa.nama_lengkap)
        title = heading+" | "
        context = {
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "datanya": datanya,
                   }
        return render(request, "penilaian/rekapun_list.html",context )
    else:
        return render(request, "403.html", {} )

def nilaiku(request):
    if request.session['hak_akses'] =="siswa":
        if "periode_id" in request.POST:
            periode_id = request.POST['periode_id']
        else:
            try:
                #periode_id = Periode.objects.latest('id').id
                periode_id = Periode.objects.filter(verifikasi=1).latest('id').id
            except: return render(request, "404.html", {} )
        periode = Periode.objects.get(id=periode_id)
        periodes= Periode.objects.filter(verifikasi=1)
        nilaisikap = NilaiSikap.objects.filter(siswa=request.session['id_user'], periode=periode_id)
        nilaiketerampilan = NilaiKeterampilan.objects.filter(siswa=request.session['id_user'], periode=periode_id)
        nilaikognitif = NilaiKognitif.objects.filter(siswa=request.session['id_user'], periode=periode_id)
        nilaitotal = NilaiTotal.objects.filter(siswa=request.session['id_user'], periode=periode_id)
        pagegroups = "penilaian"
        page = "nilaiku"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                            <li class=active>Nilai Saya Semester %s</li>" %(periode)
        heading = "Nilai Saya Semester %s" %(periode)
        title = heading+" | "
        kelas = Kelas.objects.filter(kelas_siswa__siswa__id=request.session['id_user'],\
                                     jadwal_kelas__tahun_ajaran=periode.tahun_ajaran).distinct().latest('id')
        context = {
                   "pagegroups": pagegroups,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "title": title,
                   "nilaisikap": nilaisikap,
                   "nilaiketerampilan": nilaiketerampilan,
                   "nilaikognitif": nilaikognitif,
                   "nilaitotal": nilaitotal,
                   "periodes": periodes,
                   "kelas": kelas,
                   "periode": periode,
                   }

        return render(request, "penilaian/nilaiku.html",context )
    else:
        return render(request, "403.html", {} )






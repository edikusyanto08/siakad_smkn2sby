from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from data_master.models import ThnAjaran
from penilaian.models import NilaiKompetensi
from datetime import datetime


# Create your views here.
def absen_siswa(request):
    if request.session['hak_akses'] !="siswa":
        datanya = AbsensiSiswa.objects.all()
        heading = "Absensi Siswa"
        title = heading+" | "
        pagegroups = "kesiswaan"
        page = "absensisiswa"
        buttonadd ="tambah/"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li class=active>Absensi Siswa</li>"
        context = {"heading":heading,
                   "title":title,
                   "breadcrumb": breadcrumb,
                   "datanya":datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "buttonadd":buttonadd,
                   }
        return render(request, "kesiswaan/data_abssiswa.html", context)
    else:
        return render(request, "403.html", {} )

def tambah_abs_siswa(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        heading = "Tambah Absensi Siswa"
        title = heading+" | "
        pagegroups = "kesiswaan"
        page = "absensisiswa"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a href=/kesiswaan/absensi/>Absensi Siswa</a></li>\
                    <li class=active>Tambah Data</li>"
        form = AbsensiSiswaForm(request.POST or None, request.FILES or None)
        form.fields['siswa'].queryset = Siswa.objects.filter(kelas_siswa__tahun_ajaran=ThnAjaran.objects.latest('id').id)
        linkback = "/kesiswaan/absensi/"
        context = {"heading":heading,
                   "title":title,
                   "breadcrumb": breadcrumb,
                   "form": form,
                   "pagegroups": pagegroups,
                   "page": page,
                   "linkback": linkback,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                messages.success(request,'Data telah ditambahkan')
                return redirect('absen_siswa')
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
        return render(request, "kesiswaan/add_data.html", context)
    else:
        return render(request, "403.html", {} )

def hapus_abs_siswa(request,idData):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        datanya = get_object_or_404(AbsensiSiswa, pk=idData)
        try:
            datanya.delete()
            messages.success(request,"Data telah dihapus.")
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))
        return redirect('absen_siswa')
    else:
        return render(request, "403.html", {} )

def absen_guru(request):
    if request.session['hak_akses'] !="siswa" and request.session['hak_akses'] !="guru":
        datanya = AbsensiGuru.objects.all()
        heading = "Absensi Guru"
        title = heading+" | "
        page = "absensiguru"
        pagegroups = "kepegawaian"
        buttonadd ="tambah/"
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li class=active>Absensi Guru</li>"
        context = {"heading":heading,
                   "title":title,
                   "breadcrumb": breadcrumb,
                   "datanya":datanya,
                   "pagegroups": pagegroups,
                   "page": page,
                   "buttonadd":buttonadd,
                   }
        return render(request, "kepegawaian/data_absguru.html", context)
    else:
        return render(request, "403.html", {} )

def tambah_abs_guru(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        heading = "Tambah Absensi Guru"
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a href=/kepegawaian/absensi/>Absensi Guru</a></li>\
                    <li class=active>Tambah Data</li>"
        pagegroups = "kepegawaian"
        page = "absensiguru"
        linkback = "/kepegawaian/absensi/"
        form = AbsensiGuruForm(request.POST or None, request.FILES or None)
        context = {"heading":heading,
                   "title":title,
                   "breadcrumb": breadcrumb,
                   "form": form,
                   "pagegroups": pagegroups,
                   "page": page,
                   "linkback": linkback,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                save_it.save()
                messages.success(request,'Data telah ditambahkan')
                return redirect('absen_guru')
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Data gagal ditambahkan. (%s)' %(err))
        return render(request, "kepegawaian/add_data.html", context)
    else:
        return render(request, "403.html", {} )

def hapus_abs_guru(request,idData):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        datanya = get_object_or_404(AbsensiGuru, pk=idData)
        try:
            datanya.delete()
            messages.success(request,"Data telah dihapus.")
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Data gagal dihapus. (%s)' %(err))
        return redirect('absen_guru')
    else:
        return render(request, "403.html", {} )

################################# bagian laporan #########

def laporan(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        page = "laporan"
        pagegroups = "laporan"
        heading = "Laporan"
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li class=active>Laporan</li>"
        context = {"page":page,
                   "pagegroups":pagegroups,
                   "title":title,
                   "heading":heading,
                   "breadcrumb":breadcrumb,
                   }
        return render(request, "laporan/laporan.html", context)
    else:
        return render(request, "403.html", {} )

def absensi_siswa(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        page = "absensi_siswa"
        pagegroups = "laporan"
        heading = "Laporan Absensi Siswa"
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a href=/laporan/> Laporan</a></li>\
                    <li class=active> Absensi Siswa</li>"
        context = {"page":page,
                   "pagegroups":pagegroups,
                   "title":title,
                   "heading":heading,
                   "breadcrumb":breadcrumb,
                   }
        return render(request, "laporan/rentang_waktu.html", context)
    else:
        return render(request, "403.html", {} )

def cetak_absensi_siswa(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        try:
            start = datetime.strptime(request.POST['mulai_tanggal'],'%Y-%m-%d')
            end = datetime.strptime(request.POST['sampai_tanggal'],'%Y-%m-%d')
            datanya = AbsensiSiswa.objects.filter(tanggal__range=(start, end)).order_by('tanggal')
        except:
            datanya = AbsensiSiswa.objects.filter(tanggal=datetime.now().date()).order_by('tanggal')
            start = datetime.now().date()
            end = datetime.now().date()
        heading = "Laporan Absensi Siswa"
        title = heading+" | "
        context = {
                   "title":title,
                   "heading":heading,
                   "datanya":datanya,
                   "start":start,
                   "end":end,
                   }
        return render(request, "laporan/lap_abs_siswa.html", context)
    else:
        return render(request, "403.html", {} )

def absensi_guru(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        page = "absensi_siswa"
        pagegroups = "laporan"
        heading = "Laporan Absensi Guru"
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a href=/laporan/> Laporan</a></li>\
                    <li class=active> Absensi Guru</li>"
        context = {"page":page,
                   "pagegroups":pagegroups,
                   "title":title,
                   "heading":heading,
                   "breadcrumb":breadcrumb,
                   }
        return render(request, "laporan/rentang_waktu.html", context)
    else:
        return render(request, "403.html", {} )

def cetak_absensi_guru(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        try:
            start = datetime.strptime(request.POST['mulai_tanggal'],'%Y-%m-%d')
            end = datetime.strptime(request.POST['sampai_tanggal'],'%Y-%m-%d')
            datanya = AbsensiGuru.objects.filter(tanggal__range=(start, end)).order_by('tanggal')
        except:
            datanya = AbsensiGuru.objects.filter(tanggal=datetime.now().date()).order_by('tanggal')
            start = datetime.now().date()
            end = datetime.now().date()
        heading = "Laporan Absensi Guru"
        title = heading+" | "
        context = {
                   "title":title,
                   "heading":heading,
                   "datanya":datanya,
                   "start":start,
                   "end":end,
                   }
        return render(request, "laporan/lap_abs_guru.html", context)
    else:
        return render(request, "403.html", {} )

def transkrip(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" :
        if "siswa" in request.GET:
            siswa = Siswa.objects.get(NIS=request.GET['siswa'])
        else:
            siswa = 0
        datanya = NilaiKompetensi.objects.filter(siswa=siswa)
        page = "traskrip"
        pagegroups = "laporan"
        heading = "Transkrip Kompetensi Siswa"
        title = heading+" | "
        breadcrumb = "<li><a href=/home/>Home</a></li>\
                    <li><a href=/laporan/> Laporan</a></li>\
                    <li class=active> Transkrip Kompetensi Siswa</li>"
        context = {"page":page,
                   "pagegroups":pagegroups,
                   "title":title,
                   "heading":heading,
                   "breadcrumb":breadcrumb,
                   "datanya": datanya,
                   }
        return render(request, "laporan/transkrip.html", context)
    else:
        return render(request, "403.html", {} )
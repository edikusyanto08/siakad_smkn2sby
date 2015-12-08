from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from kepegawaian.models import Guru
from kesiswaan.models import Siswa
from django.contrib import messages
from .forms import *

# Create your views here.

def login_view(request):
    try:
        if request.session['userid']:
            return redirect('home')
    except: pass
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['kelas_siswa'] = []
                if user.is_superuser:
                    request.session['nama_user'] = "Administrator"
                    request.session['hak_akses'] = "Admin"
                    request.session['id_user'] = "admin"
                    request.session['userid'] = user.id
                else:
                    try:
                        request.session['nama_user'] = user.siswa_user.nama_lengkap
                        request.session['hak_akses'] = user.first_name
                        request.session['id_user'] = user.siswa_user.id
                        request.session['userid'] = user.id
                        request.session['reg'] = user.siswa_user.NIS
                        #request.session.set_expiry(30)
                    except:
                        request.session['nama_user'] = user.guru_user.nama_lengkap
                        request.session['hak_akses'] = user.first_name
                        request.session['id_user'] = user.guru_user.id
                        request.session['userid'] = user.id
                        request.session['reg'] = user.guru_user.NIP
                        #request.session.set_expiry(30)
                if "next" in request.GET:
                    alih_page = request.GET['next']
                    return redirect(alih_page)
                else:
                    return redirect('home')
            else:
                messages.error(request,"Akun anda sedang diblokir,Silahkan hubungi admin.")
                return render(request,'login/login.html', {"page": login})
        else:
            messages.error(request,"Username atau Password salah!")
            return render(request,'login/login.html', {"page": login})
    return render(request,'login/login.html', {"page": login})

def logout_view(request):
    logout(request)
    messages.success(request, "Anda telah sukses keluar dari sistem.")
    return redirect("login")

def home(request):
    page="home"
    title = "Halaman Utama | "
    context = {"page":page,
               "title":title,
               }
    return render(request,'home.html', context)

def user(request):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf" or request.session['hak_akses'] =="kepsek" :
        if "q" in request.GET:
            keyword = request.GET['q']
            queryset = Q(username__icontains=keyword) | Q(guru_user__nama_lengkap__icontains=keyword) | Q(siswa_user__nama_lengkap__icontains=keyword)\
            | Q(first_name__icontains=keyword)
            datanya = User.objects.filter(queryset, is_superuser=0)
        else:
            datanya=User.objects.filter(is_superuser=0)
        paginator = Paginator(datanya, 20)
        if "hal" in request.GET:
            hal = request.GET['hal']
        else:
            hal = 1
        total_data = paginator.count
        try:
            usernya = paginator.page(hal)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            usernya = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            usernya = paginator.page(paginator.num_pages)
        page = "user"
        breadcrumb = "<li><a href=/home/>Home</a></li><li class=active>Data User</li>"
        heading = "Data User"
        title = heading+" | "
        linkubah = "reset/"
        linkhapus = "blokir/"
        context = {"usernya": usernya,
                   "page": page,
                   "breadcrumb": breadcrumb,
                   "heading": heading,
                   "linkubah": linkubah,
                   "title": title,
                   "linkhapus": linkhapus,
                   "total_data":total_data,
        }

        return render(request, "login/view_user.html", context )
    else:
        return render(request, "403.html", {} )

def reset_password(request,idUser):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf":
        usernya = User.objects.get(id=idUser)

        heading = 'Ubah Password User' #utk panel header
        title = heading+" | "
        form = UbahPasswordForm(request.POST or None, request.FILES or None, instance=usernya)
        context = {"heading": heading,
                   "form": form,
                   "title": title,
                   }
        if form.is_valid():
            save_it = form.save(commit=False)
            try:
                pswd = form.cleaned_data['password']
                save_it.save()
                usernya.set_password(pswd)
                usernya.save()
                messages.success(request,'Password telah diubah')
                [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == usernya.id] #paksa user logout
                if "done" in request.GET:
                    rendernya = "onload=refreshAndClose()"
                    context={"rendernya": rendernya,}
                    return render(request, 'login/popup_password.html', context)
            except BaseException, err:
                messages.error(request,'Terjadi kesalahan! Password gagal diubah. (%s)' %(err))
        return render(request, 'login/popup_password.html', context)
    else:
        return render(request, "403.html", {} )

def blokir_user(request, idUser):
    if request.session['hak_akses'] =="Admin" or request.session['hak_akses'] =="staf":
        usernya = get_object_or_404(User, pk=idUser)
        [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == usernya.id] #paksa user logout
        if usernya.is_active==1:
            usernya.is_active=0
            usernya.save()
            messages.success(request,"User telah diblokir")
        else:
            usernya.is_active=1
            usernya.save()
            messages.success(request,"User telah diaktifkan")
        return redirect("user")
    else:
        return render(request, "403.html", {} )

def ubah_password(request):
    usernya = get_object_or_404(User, pk=request.session['userid'])
    heading = 'Ubah Password User' #utk panel header
    title = heading+" | "
    form = UserUbahPasswordForm(usernya, request.POST or None,)
    context = {"form": form,
               "usernya": usernya,
               "title":title,
               }
    if form.is_valid():
        try:
            pswd = form.cleaned_data['password_baru']
            usernya.set_password(pswd)
            usernya.save()
            messages.success(request,'Password telah diubah')
            if "done" in request.GET:
                rendernya = "onload=refreshAndClose()"
                context={"rendernya": rendernya,}
                return render(request, 'login/popup_password.html', context)
        except BaseException, err:
            messages.error(request,'Terjadi kesalahan! Password gagal diubah. (%s)' %(err))
    return render(request, 'login/popup_password.html', context)

def detil_user(request, Username):
    try:
        guru = Guru.objects.get(NIP=Username).id
        return redirect("/kepegawaian/guru/detil/%d" %(guru))
    except:
        siswa = Siswa.objects.get(NIS=Username).id
        return redirect("/kesiswaan/siswa/detil/%d" %(siswa))
    return redirect("user")

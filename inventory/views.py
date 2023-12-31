from django.shortcuts import render, get_object_or_404, redirect
from .models import Barang, Ormawa, Transaksi, RequestPeminjaman, User
from .forms import PeminjamanForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import datetime


@receiver(post_save, sender=Transaksi)
def update_jml_stok(sender, instance, created, **kwargs):
    if instance.status == 'setuju':
        pesanan = instance.id_request
        barang = pesanan.barang
        barang.jml_stok -= pesanan.jumlah
        barang.save()

@receiver(post_save, sender=RequestPeminjaman)
def update_jml_stok_kembali(sender, instance, created, **kwargs):
    # print('tanggal kiri', timezone.now(), 'tanggal kanan', datetime.strptime(instance.tgl_kembali, '%Y-%m-%d'))
    print('tanggal kiri', timezone.now(), 'tanggal kanan', instance.tgl_kembali)
    
    if datetime.now() >= instance.tgl_kembali:
        barang = instance.barang
        barang.jml_stok = int(barang.jml_stok) + int(instance.jumlah)
        barang.save()

# memastikan untuk melewati proses login dahulu
@login_required
def index(request):
    # mengambil data tabel barang dan disimpan di variable brg
    brg = Barang.barang_listed.all()
    # mengambil data tabel ormawa dan disimpan di variable ormawa
    ormawa = Ormawa.organisasi.all()
    # mengambil data tabel RequestPeminjaman dan disimpan di variable peminjaman
    peminjaman = RequestPeminjaman.request_listed.all()
    # mengambil data tabel Transaksi dan disimpan di variable transaksi
    transaksi = Transaksi.transaksi.all()
    # mengembalikan nilai data dari tabel barang, ormawa, request peminjaman dan transaksi ke halaman index.html
    print(request.user.id)
    barang_pinjam = Ormawa.objects.filter(user_id= request.user.id).values('id_ormawa')

    # id_ormawa = None
    for a in barang_pinjam:
        id_ormawa = a['id_ormawa']

    print('barang', barang_pinjam)
    print('id_ormawa', id_ormawa)

    peminjaman_user = RequestPeminjaman.objects.filter(ormawa_id= id_ormawa)
    # print(peminjaman_user.cleaned_data['barang_id'])

    return render(request, 'index.html', {'Barang': brg, 'Ormawa': ormawa, 'RequestPeminjaman': peminjaman_user, 'Transaksi': transaksi })

@login_required
def peminjaman(request):
    ormawa_listed = Ormawa.objects.all()  # Mendapatkan semua data ormawa
    barang_listed = Barang.objects.all()  # Mendapatkan semua data barang
    transaksi = Transaksi.objects.all()

    if request.method == 'POST':
        form = PeminjamanForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ormawa = get_object_or_404(Ormawa, id_ormawa=cd['ormawa'])
            barang = get_object_or_404(Barang, id_barang=cd['barang'])
            # Buat objek Pesanan baru
            pesanan = RequestPeminjaman.objects.create(
                ormawa=ormawa,
                barang=barang,
                jumlah=cd['jumlah'],
                tgl_pinjam=cd['tgl_pinjam'],
                tgl_kembali=cd['tgl_kembali']
            )
            pesan = "Formulir peminjaman berhasil dikirim."

            return render(request, 'peminjaman_barang.html', {'form': form, 'pesan': pesan, 'ormawa_listed': ormawa_listed, 'barang_listed': barang_listed, 'Transaksi': transaksi})
    else:
        form = PeminjamanForm()

    return render(request, 'peminjaman_barang.html', {'form': form, 'ormawa_listed': ormawa_listed, 'barang_listed': barang_listed, 'Transaksi': transaksi})


def update_request(request, request_id):
    request_obj = RequestPeminjaman.objects.get(pk=request_id)
    if request.method == 'POST':
        # Ambil data yang diupdate dari form
        jumlah = request.POST.get('jumlah', None)
        tanggal = request.POST.get('tanggal', None)

        if jumlah is not None and tanggal is not None:
            # Update data peminjaman
            request_obj.jumlah = jumlah
            request_obj.tgl_kembali = tanggal
            request_obj.save()
            return redirect('index')
        else:
            # Tindakan yang sesuai jika 'jumlah' atau 'tanggal' tidak ada
            # Misalnya, menampilkan pesan kesalahan kepada pengguna
            error_message = "Silakan isi jumlah dan tanggal."
            return render(request, 'update_request.html', {'request': request_obj, 'error_message': error_message})

    return render(request, 'update_request.html', {'request': request_obj})


def delete_request(request, request_id):
    if request.method == 'POST':
        request_obj = RequestPeminjaman.objects.get(pk=request_id)
        request_obj.delete()
    return redirect('index')

def kembali_barang(request):
    if request.method == 'POST':
        request_id = request.POST['request_id']
        request_obj = RequestPeminjaman.objects.get(pk=request_id)
        pesanan = get_object_or_404(RequestPeminjaman, pk=request_id)
        print("Pesanan:", pesanan)
        if timezone.now() >= pesanan.tgl_kembali:
            barang = pesanan.barang
            barang.jml_stok += pesanan.jumlah
            barang.save()
        return redirect('index')
    return redirect('index')
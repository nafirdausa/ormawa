from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class BarangManager(models.Manager):
    def get_queryset(self):
        return super(BarangManager, self).get_queryset()

# data ormawa yg sesuai dg prodi
class OrmawaManager(models.Manager):
    def get_queryset(self, prodi):
        return super(OrmawaManager, self).get_queryset().filter(prodi=prodi)
    # SELECT * FROM OrmawaManager
    # WHERE prodi = 'prodi'

# data pesanan yg sesuai dg ormawa & barang
class PesananManager(models.Manager):
    def get_queryset(self, barang, ormawa):
        return super(PesananManager, self).get_queryset().filter(barang=barang, ormawa=ormawa)
    # SELECT * FROM PesananManager
    # WHERE barang = 'barang' and ormawa='ormawa'

# data transaksi yg sesuai dg pesanan
class TransaksiManager(models.Manager):
    def get_queryset(self, id_request):
        return super(TransaksiManager, self).get_queryset().filter(id_request=id_request)
    # SELECT * FROM TransaksiManager
    # WHERE barang = 'barang'


# Create your models here.
class UnitKerja(models.Model):
    nama_unitKerja = models.CharField(max_length=255)

class Ormawa(models.Model):
    #default manager
    objects = models.Manager()
    # object/instance
    organisasi = BarangManager()

    id_ormawa = models.CharField(max_length=50, primary_key=True)
    unitkerja = models.ForeignKey(UnitKerja, on_delete=models.CASCADE)
    nama_ormawa = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_hp = models.CharField(max_length=16)

class Barang(models.Model):
    #default manager
    objects = models.Manager()
    # object/instance
    barang_listed = BarangManager()

    id_barang = models.CharField(max_length=50, primary_key=True)
    nama_barang = models.CharField(max_length=255)
    jml_stok = models.IntegerField()

class RequestPeminjaman(models.Model):
    # default manager
    objects = models.Manager()
    # object/instance
    request_listed = BarangManager()

    ormawa = models.ForeignKey(Ormawa, on_delete=models.CASCADE)
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    jumlah = models.IntegerField(default=0)
    tgl_pinjam = models.DateTimeField(default=timezone.now)
    tgl_kembali = models.DateTimeField()


class Transaksi(models.Model):
    #default manager
    objects = models.Manager()
    # object/instance
    transaksi = BarangManager()

    id_request = models.ForeignKey("RequestPeminjaman", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=(('setuju', 'Disetujui'), ('ditolak', 'Ditolak')))
    alasan = models.CharField(max_length=225)

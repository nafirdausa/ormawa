from django.contrib import admin
from .models import UnitKerja, Barang, Ormawa, Transaksi, RequestPeminjaman

# Register your models here.
@admin.register(UnitKerja)
class UKAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_unitKerja')

@admin.register(Ormawa)
class OrmawaAdmin(admin.ModelAdmin):
    list_display = ('id_ormawa', 'unitkerja', 'nama_ormawa', 'user', 'no_hp', 'user_id')
    list_filter =('unitkerja', 'nama_ormawa')
    search_fields = ('unitkerja', 'nama_ormawa')
    raw_id_fields = ('unitkerja',)

@admin.register(Barang)
class BarangAdmin(admin.ModelAdmin):
    list_display = ('id_barang', 'nama_barang', 'jml_stok')
    list_filter =('nama_barang','jml_stok')
    search_fields = ('nama_barang','jml_stok')


@admin.register(RequestPeminjaman)
class PesananAdmin(admin.ModelAdmin):
    list_display = ('id', 'barang', 'jumlah', 'ormawa', 'tgl_pinjam', 'tgl_kembali')
    list_filter =('barang', 'ormawa','tgl_pinjam', 'tgl_kembali')
    search_fields = ('barang', 'ormawa')
    raw_id_fields = ('ormawa','barang',)
    date_hierarchy = 'tgl_pinjam'

@admin.register(Transaksi)
class TransaksiAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_request', 'status', 'alasan')
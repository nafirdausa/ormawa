from django import forms
from .models import RequestPeminjaman

class PeminjamanForm(forms.Form):
    ormawa = forms.CharField(max_length=50)
    barang = forms.CharField(max_length=50)
    jumlah = forms.IntegerField()
    tgl_pinjam = forms.DateTimeField()
    tgl_kembali = forms.DateTimeField()


class RequestForm(forms.ModelForm):
    class Meta:
        model = RequestPeminjaman
        fields = ['jumlah', 'tgl_kembali']
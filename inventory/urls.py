from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.index, name='index'),
    path('/peminjaman', views.peminjaman, name='peminjaman'),
    path('kembali_barang/', views.kembali_barang, name='kembali_barang'),
    path('request/<int:request_id>/', views.update_request, name='update_request'),
    path('delete/<int:request_id>/', views.delete_request, name='delete_request'),
]
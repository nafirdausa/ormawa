from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.form, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
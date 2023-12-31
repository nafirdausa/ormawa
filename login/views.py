from django.shortcuts import render, redirect
from django.contrib.auth  import authenticate, login, logout
from .forms import FormLogin
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# Create your views here

@csrf_exempt
def form(request):
    form = FormLogin()
    
    if request.method == 'POST':
        username_login = request.POST['username']
        password_login = request.POST['password']

        user = authenticate(request, username = username_login, password = password_login)

        if user is not None:
            login(request, user)
            return redirect('/inventory/')
        else:
            messages.add_message(request, messages.INFO, 'Username dan Passowrd anda salah')


    return render(request, "login.html", {'form' : form})


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if email == '' or password == '':
            messages.error(request, 'Os campos email e senha não podem ser vazios')
            return redirect('usuarios:login')

        if User.objects.filter(email=email).exists():
            username = User.objects.get(email=email).username
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('lojas:lojas_list')
        else:
            messages.error(request, 'Usuário não cadastrado')

    return render(request, 'usuarios/login.html')


def logout(request):
    auth.logout(request)
    return redirect('usuarios:login')

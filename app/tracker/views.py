from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import RegisterForm, LoginForm
from django.http import HttpResponseForbidden


def register_view(request):
    """Регистрация пользователя"""
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('dashboard') 
    else:
        form = RegisterForm()
    
    return render(request, 'tracker/register.html', {'form': form})


def login_view(request):
    """Вход пользователя"""
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Неверное имя пользователя или пароль")
    else:
        form = LoginForm()
    
    return render(request, 'tracker/login.html', {'form': form})


def logout_view(request):
    """Выход пользователя"""
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    """Главная страница (дашборд)"""
    return render(request, 'tracker/dashboard.html')

def custom_403(request, exception):
    """Пользовательская страница ошибки 403"""
    return render(request, 'tracker/403.html', status=403)

def test_403(request):
    """Тестовая страница для проверки 403"""
    return render(request, 'tracker/403.html', status=403)
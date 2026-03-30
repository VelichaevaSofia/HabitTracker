from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """Форма регистрации"""
    
    email = forms.EmailField(required=True, label="Email")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы для стилей
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class LoginForm(forms.Form):
    """Форма входа"""
    
    username = forms.CharField(max_length=100, label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
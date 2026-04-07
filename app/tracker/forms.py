from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """Форма регистрации"""
    
    email = forms.EmailField(
    required=True, 
    label="Email",
    error_messages={
        'invalid': 'Введите корректный email (например, user@mail.ru)',
        'required': 'Введите email',
    }
)
    
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
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
       
        email = self.cleaned_data.get('email')
        from django.contrib.auth.models import User
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован")

        import re
        if not re.search(r'@\w+\.\w+', email):
            raise forms.ValidationError("Некорректный формат email (например user@mail.ru)")
        
        return email



class LoginForm(forms.Form):
    """Форма входа"""
    
    username = forms.CharField(max_length=100, label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Habit, Profile


class RegisterForm(UserCreationForm):  
    email = forms.EmailField(
        required=True, 
        label="Email",
        error_messages={
            'invalid': 'Введите правильный email (например, user@mail.ru)',
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
    username = forms.CharField(max_length=100, label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class HabitForm(forms.ModelForm):
    custom_category = forms.CharField(
        max_length=50,
        required=False,
        label="Своя категория ('Другое')",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введи свою категорию'})
    )

    schedule_type = forms.ChoiceField(
        choices=[
            ('daily', 'Ежедневно'),
            ('weekdays', 'По будням (Пн-Пт)'),
            ('weekends', 'По выходным (Сб-Вс)'),
            ('custom', 'Выбрать дни'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Расписание",
        initial='daily'
    )

    days_of_week = forms.MultipleChoiceField(
        choices=[
            (0, 'Понедельник'),
            (1, 'Вторник'),
            (2, 'Среда'),
            (3, 'Четверг'),
            (4, 'Пятница'),
            (5, 'Суббота'),
            (6, 'Воскресенье'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Выберите дни"
    )

    class Meta:
        model = Habit
        fields = ['name', 'description', 'category', 'schedule_type', 'days_of_week']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'category': 'Категория',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'maxlength': 500,
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'email', 'email_notifications']
        labels = {
            'avatar': 'Аватарка',
            'bio': 'О себе',
            'email': 'Email для уведомлений',
            'email_notifications': 'Получать уведомления на email',
        }
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'maxlength': 500,
                'placeholder': 'Расскажите о себе...'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PasswordChangeForm(forms.Form):

    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Текущий пароль"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Новый пароль"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Подтверждение нового пароля"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Пароли не совпадают")
        
        return cleaned_data


class ReminderSettingsForm(forms.ModelForm):
    
    class Meta:
        model = Habit
        fields = ['reminder_enabled', 'reminder_time']
        labels = {
            'reminder_enabled': 'Включить напоминания',
            'reminder_time': 'Время напоминания',
        }
        widgets = {
            'reminder_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'reminder_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
        }
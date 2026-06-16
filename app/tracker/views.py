from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden
from .forms import RegisterForm, LoginForm, HabitForm,  ProfileForm, PasswordChangeForm
from .services import AuthService, HabitService, CompletionService
from .models import Habit, HabitCompletion, Profile
from tracker.services.email_service import send_reminder_email
from tracker.forms import ReminderSettingsForm


def register_view(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = AuthService.register_user(form)
            AuthService.login_user(request, user)
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
            user = AuthService.authenticate_user(username, password)
            
            if user is not None:
                AuthService.login_user(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Неверное имя пользователя или пароль")
    else:
        form = LoginForm()
    
    return render(request, 'tracker/login.html', {'form': form})


def logout_view(request):
    """Выход пользователя"""
    AuthService.logout_user(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    """Дашборд"""
    all_habits = HabitService.get_user_habits(request.user)
    
    selected_category = request.GET.get('category', 'all')
    
    if selected_category == 'other':
        standard_categories = ['health', 'sport', 'study', 'hobby']
        habits = all_habits.exclude(category__in=standard_categories)
    elif selected_category != 'all':
        habits = all_habits.filter(category=selected_category)
    else:
        habits = all_habits
    
    
    today = timezone.now().date()
    
    day_names = {
        0: 'Пн', 1: 'Вт', 2: 'Ср', 3: 'Чт', 
        4: 'Пт', 5: 'Сб', 6: 'Вс',
        '0': 'Пн', '1': 'Вт', '2': 'Ср', '3': 'Чт', 
        '4': 'Пт', '5': 'Сб', '6': 'Вс'
    }
    
    for habit in habits:
        habit.completed_today = HabitCompletion.objects.filter(
            habit=habit,
            user=request.user,
            date=today
        ).exists()
        
        if habit.days_of_week:
            try:
                sorted_days = sorted([int(d) for d in habit.days_of_week])
            except (ValueError, TypeError):
                sorted_days = []
            
            if len(sorted_days) == 7:
                habit.days_display = "Ежедневно"
            elif len(sorted_days) == 0:
                habit.days_display = "Не выбрано"
            else:
                habit.days_display = ", ".join([day_names[d] for d in sorted_days])
        else:
            habit.days_display = "Не выбрано"
    
    return render(request, 'tracker/dashboard.html', {
        'habits': habits,
        'selected_category': selected_category,
    })


def custom_403(request, exception):
    """Страница ошибки 403"""
    return render(request, 'tracker/403.html', status=403)


def test_403(request):
    """Тестовая страница для проверки 403"""
    return render(request, 'tracker/403.html', status=403)


@login_required
def create_habit(request):
    """Создание привычки"""
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            HabitService.create_habit(request.user, form)
            return redirect('dashboard')
    else:
        form = HabitForm()
    
    return render(request, 'tracker/create_habit.html', {'form': form})


@login_required
def delete_habit(request, habit_id):
    """Удаление привычки"""
    habit = HabitService.get_habit_by_id(habit_id, request.user)
    HabitService.delete_habit(habit)
    return redirect('dashboard')


@login_required
def edit_habit(request, habit_id):
    """Редактирование привычки"""
    habit = HabitService.get_habit_by_id(habit_id, request.user)
    
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            HabitService.update_habit(habit, form)
            return redirect('dashboard')
    else:
        form = HabitForm(instance=habit)
        
        from .models import Habit
        if habit.category not in dict(Habit.CATEGORY_CHOICES):
            form.initial['category'] = 'other'
            form.initial['custom_category'] = habit.category
    
    return render(request, 'tracker/edit_habit.html', {'form': form})


@login_required
def complete_habit(request, habit_id):
    """Отметка выполнения привычки"""
    habit = HabitService.get_habit_by_id(habit_id, request.user)
    CompletionService.toggle_completion(habit, request.user)
    return redirect('dashboard')

@login_required
def profile_view(request):
    """Страница профиля"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST' and 'profile_form' in request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    password_form = PasswordChangeForm()
    
    context = {
        'form': form,
        'password_form': password_form,
    }
    
    return render(request, 'tracker/profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password1')
            
            if not user.check_password(current_password):
                form.add_error('current_password', 'Неверный текущий пароль')
            else:
                user.set_password(new_password)
                user.save()
                return redirect('profile')
    else:
        form = PasswordChangeForm()
    
    return render(request, 'tracker/profile.html', {'password_form': form})

from datetime import timedelta
from calendar import monthrange

@login_required
def calendar_view(request, year=None, month=None):
    from django.utils import timezone
    from calendar import monthrange
    
    today = timezone.now()

    if request.GET.get('month'):
        month = int(request.GET.get('month'))
    if request.GET.get('year'):
        year = int(request.GET.get('year'))
    
    if year is None or month is None:
        current_date = today
        year = current_date.year
        month = current_date.month
    else:
        current_date = timezone.datetime(year, month, 1)
    
    if year and month:
        current_date = timezone.datetime(year, month, 1)
    else:
        current_date = today
        
    year = current_date.year
    month = current_date.month
    
    first_day, num_days = monthrange(year, month)
    
    days_in_month = []
    for day in range(1, num_days + 1):
        date = timezone.datetime(year, month, day).date()
        day_of_week = date.weekday()  
        
        habits_for_day = []
        habits = Habit.objects.filter(user=request.user)
        
        for habit in habits:
            habit_days = [int(d) for d in habit.days_of_week] if habit.days_of_week else []
            
            if day_of_week in habit_days:
                is_completed = HabitCompletion.objects.filter(
                    habit=habit,
                    user=request.user,
                    date=date
                ).exists()
                
                habits_for_day.append({
                    'habit': habit,
                    'is_completed': is_completed
                })
        
        days_in_month.append({
            'date': date,
            'day_number': day,
            'day_of_week': day_of_week,
            'habits': habits_for_day
        })
    
    month_names = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
        5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
        9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }
    
    day_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year
        
    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year
    
    current_year = today.year
    years_range = range(current_year - 5, current_year + 10)
    
    context = {
        'year': year,
        'month': month,
        'month_name': month_names[month],
        'day_names': day_names,
        'days_in_month': days_in_month,
        'first_day': first_day,
        'empty_days': range(first_day) if first_day > 0 else [],
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'years_range': years_range,
    }
    
    return render(request, 'tracker/calendar.html', context)

@login_required
def today_view(request):
    """Страница привычки на сегодня"""
    from django.utils import timezone
    
    today = timezone.now().date()
    day_of_week = today.weekday()  

    habits = Habit.objects.filter(user=request.user)
    
    today_habits = []
    for habit in habits:
        habit_days = [int(d) for d in habit.days_of_week] if habit.days_of_week else []
        
        if day_of_week in habit_days:
            is_completed = HabitCompletion.objects.filter(
                habit=habit,
                user=request.user,
                date=today
            ).exists()
            
            today_habits.append({
                'habit': habit,
                'is_completed': is_completed
            })
    
    total = len(today_habits)
    completed = sum(1 for h in today_habits if h['is_completed'])
    progress_percent = (completed / total * 100) if total > 0 else 0
    
    day_names_full = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    
    context = {
        'today': today,
        'day_name': day_names_full[day_of_week],
        'today_habits': today_habits,
        'total': total,
        'completed': completed,
        'progress_percent': progress_percent,
    }
    
    return render(request, 'tracker/today.html', context)


@login_required
def toggle_habit_completion(request, habit_id):
    """Выполнено/не выполнено"""
    from django.utils import timezone
    from django.http import JsonResponse
    
    today = timezone.now().date()
    habit = Habit.objects.get(id=habit_id, user=request.user)
    
    completion = HabitCompletion.objects.filter(
        habit=habit,
        user=request.user,
        date=today
    ).first()
    
    if completion:
        completion.delete()
        is_completed = False
    else:
        HabitCompletion.objects.create(
            habit=habit,
            user=request.user,
            date=today
        )
        is_completed = True
    
    return JsonResponse({
        'is_completed': is_completed,
        'habit_id': habit_id
    })


@login_required
def reminder_settings_view(request, habit_id):
    """Страница настройки напоминаний для привычки"""
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    
    if request.method == 'POST':
        form = ReminderSettingsForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            if habit.reminder_enabled:
                send_reminder_email(habit)
            return redirect('dashboard')
    else:
        form = ReminderSettingsForm(instance=habit)
    
    return render(request, 'tracker/reminder_settings.html', {
        'form': form,
        'habit': habit
    })
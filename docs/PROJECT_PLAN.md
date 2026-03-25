План проекта HabitTracker!!!!!!!

Web-приложение для отслеживания и формирования полезных привычек с визуализацией прогресса и системой мотивации



Экраны приложения:

1. Register (Регистрация)
- **URL:** `/register/`
- **Template:** `registration/register.html`
- **View:** `tracker/views.py` - `register_view()`
- **Form:** `tracker/forms.py` - `UserRegistrationForm`

2. Login (Вход)
- **URL:** `/login/`
- **Template:** `registration/login.html`
- **View:** Django built-in `LoginView`

3. Dashboard (Главная)
- **URL:** `/` или `/dashboard/`
- **Template:** `tracker/dashboard.html`
- **View:** `tracker/views.py` - `dashboard_view()`

4. Create Habit (Создание привычки)
- **URL:** `/habits/create/`
- **Template:** `tracker/habit_form.html`
- **View:** `tracker/views.py` - `HabitCreateView`
- **Form:** `tracker/forms.py` - `HabitForm`

5. Habit List (Список привычек)
- **URL:** `/habits/`
- **Template:** `tracker/habit_list.html`
- **View:** `tracker/views.py` - `HabitListView

6. Edit Habit (Редактирование)
- **URL:** `/habits/<int:pk>/edit/`
- **Template:** `tracker/habit_form.html`
- **View:** `tracker/views.py` - `HabitUpdateView`

7. Delete Habit (Удаление)
- **URL:** `/habits/<int:pk>/delete/`
- **Template:** `tracker/habit_confirm_delete.html`
- **View:** `tracker/views.py` - `HabitDeleteView`

8. Mark Complete (Отметка выполнения)
- **URL:** `/habits/<int:habit_id>/toggle/`
- **View:** `tracker/views.py` - `toggle_habit_completion()`
- **Model:** `HabitLog`

9. Statistics (Статистика)
- **URL:** `/statistics/`
- **Template:** `tracker/statistics.html`
- **View:** `tracker/views.py` - `statistics_view()`

10. Profile (Профиль)
- **URL:** `/profile/`
- **Template:** `tracker/profile.html`
- **View:** `tracker/views.py` - `profile_view()`

11. Logout (Выход)
- **URL:** `/logout/`
- **View:** Django built-in `LogoutView`




!! Модели базы данных !!

1. User 
- id
- username
- email
- password 
- date_join

2. Habit (Привычка)
- id (primary Key)
- user (ForeignKey - User)
- title (название)
- description (описание)
- category (категория привычки)
- frequency (ежедневно/еженедельно)
- created_at (дата создания)
- updated_at (дата обновления)

Методы:
- get_streak() - текущая серия дней
- get_best_streak() - лучшая серия
- is_completed_today() - выполнена ли она сегодня

3. HabitLog (Журнал выполнений)
- id (Primary Key)
- habit (ForeignKey - Habit)
- date (дата выполнения)
- completed (статус: выполнено или нет)
- created_at (время записи)


!! Технический стек !!

Backend:
- Python
- Django (MVT архитектура)
- SQLite 

Frontend:
- HTML5 + CSS3
- Bootstrap 5 
- JavaScript 
- Chart.js (графики)

Deployment:
- GitHub 
- PythonAnywhere (хостинг)



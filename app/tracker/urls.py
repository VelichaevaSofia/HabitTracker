from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('', views.dashboard_view, name='home'),
    path('test-403/', views.test_403, name='test_403'),
    path('create/', views.create_habit, name= 'create_habit'),
    path('habit/<int:habit_id>/delete/', views.delete_habit, name='delete_habit'),
    path('habit/<int:habit_id>/edit/', views.edit_habit, name='edit_habit'),
    path('habit/<int:habit_id>/complete/', views.complete_habit, name='complete_habit'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar_month'),
    path('today/', views.today_view, name='today'),
    path('habit/<int:habit_id>/toggle/', views.toggle_habit_completion, name='toggle_habit'),
    path('habit/<int:habit_id>/reminders/', views.reminder_settings_view, name='reminder_settings'),
]

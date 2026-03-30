from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Habit(models.Model):
    """Модель привычки"""
    
    CATEGORY_CHOICES = [
        ('health', 'Здоровье'),
        ('sport', 'Спорт'),
        ('study', 'Учеба'),
        ('hobby', 'Хобби'),
        ('other', 'Другое'),
    ]
    
    FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
    ]
    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=100, verbose_name="Название")  
    description = models.TextField(blank=True, verbose_name="Описание")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other', verbose_name="Категория")
    how_often = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily', verbose_name="Частота")  
    
    
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")  
    
    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ['-created']  
    
    def __str__(self):
        return self.name  
    
    def get_streak(self):
        """Подсчёт текущей серии дней"""
        logs = self.logs.filter(completed=True).order_by('-date') 
        if not logs:
            return 0
        
        streak = 0
        today = timezone.now().date()
        
        for i, log in enumerate(logs):
            if i == 0 and log.date == today:
                streak = 1
            elif i == 0 and log.date == today - timezone.timedelta(days=1):
                streak = 1
            elif log.date == logs[i-1].date - timezone.timedelta(days=1):
                streak += 1
            else:
                break
        
        return streak
    
    def get_best_streak(self):
        """Подсчёт лучшей серии"""
        logs = self.logs.filter(completed=True).order_by('date')  
        if not logs:
            return 0
        
        best_streak = 1
        current_streak = 1
        
        for i in range(1, len(logs)):
            if logs[i].date == logs[i-1].date + timezone.timedelta(days=1):
                current_streak += 1
                best_streak = max(best_streak, current_streak)
            else:
                current_streak = 1
        
        return best_streak
    
    def is_completed_today(self):
        """Проверка, выполнена ли привычка сегодня"""
        today = timezone.now().date()
        return self.logs.filter(date=today, completed=True).exists()  


class HabitLog(models.Model):
    """Журнал выполнений привычек"""
    
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs') 
    date = models.DateField(verbose_name="Дата")
    done = models.BooleanField(default=True, verbose_name="Выполнено") 
    created = models.DateTimeField(auto_now_add=True, verbose_name="Время записи") 
    
    class Meta:
        verbose_name = "Запись журнала"
        verbose_name_plural = "Записи журнала"
        unique_together = ['habit', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.habit.name} - {self.date}" 
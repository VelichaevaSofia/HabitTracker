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
    
    
    days_of_week = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Дни недели"
    )
    
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")  

        
    reminder_enabled = models.BooleanField(default=False, verbose_name="Включить напоминания")
    reminder_time = models.TimeField(null=True, blank=True, verbose_name="Время напоминания")
   
    is_paused = models.BooleanField(default=False, verbose_name="Приостановлена")
    pause_start = models.DateField(null=True, blank=True, verbose_name="Начало паузы")
    pause_end = models.DateField(null=True, blank=True, verbose_name="Конец паузы")
    
    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ['-created']  
    
    def __str__(self):
        return self.name  


class HabitCompletion(models.Model):
    """Модель выполнения привычки"""
    habit = models.ForeignKey(
        Habit, 
        on_delete=models.CASCADE, 
        related_name='completions'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['habit', 'user', 'date']  
        verbose_name = 'Выполнение привычки'
        verbose_name_plural = 'Выполнения привычек'
    
    def __str__(self):
        return f"{self.habit.name} - {self.date}"


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватарка")
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    email = models.EmailField(blank=True, null=True, verbose_name="Email для уведомлений")
    email_notifications = models.BooleanField(default=True, verbose_name="Email уведомления")
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
    
    def __str__(self):
        return f"Профиль {self.user.username}"


class ReminderLog(models.Model):
    """Лог отправки напоминаний"""
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='reminder_logs')
    sent_date = models.DateField(verbose_name="Дата отправки")
    sent_time = models.TimeField(verbose_name="Время отправки")
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Лог напоминаний"
        verbose_name_plural = "Логи напоминаний"
        ordering = ['-created']
    
    def __str__(self):
        return f"Напоминание: {self.habit.name} ({self.sent_date})"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создаёт профиль при регистрации пользователя"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль при обновлении пользователя"""
    instance.profile.save()
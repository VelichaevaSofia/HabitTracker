from django.core.management.base import BaseCommand
from django.utils import timezone
from tracker.models import Habit, ReminderLog
from tracker.services.email_service import send_reminder_email
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Отправляет email-напоминания о привычках'

    def handle(self, *args, **options):
        now = timezone.localtime(timezone.now())
        current_time = now.time()
        current_day = now.weekday()  
        
        self.stdout.write(f'Проверка напоминаний ({now.strftime("%Y-%m-%d %H:%M")})')
        
        habits = Habit.objects.filter(
            reminder_enabled=True,
            reminder_time__isnull=False,
            is_paused=False,
            user__profile__email_notifications=True
        )
        
        sent_count = 0
        skipped_count = 0
        
        for habit in habits:
            if current_day not in habit.days_of_week:
                skipped_count += 1
                continue
            
            if ReminderLog.objects.filter(
                habit=habit,
                sent_date=now.date()
            ).exists():
                self.stdout.write(f'Пропущено (уже отправлено): {habit.name}')
                skipped_count += 1
                continue
            
            reminder_time = habit.reminder_time
            send_time = (datetime.combine(datetime.today(), reminder_time) - timedelta(minutes=10)).time()
            
            if current_time >= send_time and current_time < reminder_time:
                self.stdout.write(f'Отправка: {habit.name} ({habit.user.username})')
                self.stdout.write(f' Время привычки: {reminder_time.strftime("%H:%M")}')
                self.stdout.write(f' Время отправки: {send_time.strftime("%H:%M")}')
                
                if send_reminder_email(habit):
                    ReminderLog.objects.create(
                        habit=habit,
                        sent_date=now.date(),
                        sent_time=current_time
                    )
                    sent_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Отправлено: {habit.name}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Ошибка: {habit.name}'))
            else:
                skipped_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'\n Готово! Отправлено: {sent_count}, Пропущено: {skipped_count}'
        ))
from django.core.mail import send_mail
from django.conf import settings

def send_reminder_email(habit):
    subject = f"Напоминание: {habit.name}"
    message = f"Привет! Не забудь выполнить привычку '{habit.name}' сегодня\n\n{habit.description}"
    profile = habit.user.profile
    recipient_email = profile.email if profile and profile.email else habit.user.email
    recipient_list = [recipient_email] if recipient_email else []

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=f'HabitTracker <{settings.EMAIL_HOST_USER}>',
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
        return False
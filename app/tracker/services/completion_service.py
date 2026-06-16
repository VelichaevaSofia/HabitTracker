from django.utils import timezone
from ..models import HabitCompletion


class CompletionService:
    
    @staticmethod
    def toggle_completion(habit, user):
        today = timezone.now().date()
        
        completion = HabitCompletion.objects.filter(
            habit=habit,
            user=user,
            date=today
        ).first()
        
        if completion:
            completion.delete()
            return False
        else:
            HabitCompletion.objects.create(
                habit=habit,
                user=user,
                date=today
            )
            return True
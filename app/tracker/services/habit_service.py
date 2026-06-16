from django.shortcuts import get_object_or_404
from ..models import Habit


class HabitService:
    
    @staticmethod
    def get_user_habits(user):
        return Habit.objects.filter(user=user)
    
    @staticmethod
    def get_habit_by_id(habit_id, user):
        return get_object_or_404(Habit, id=habit_id, user=user)
    
    @staticmethod
    def create_habit(user, form):
        habit = form.save(commit=False)
        habit.user = user
        
        if habit.category == 'other':
            custom_category = form.cleaned_data.get('custom_category')
            if custom_category:
                habit.category = custom_category
        
        schedule_type = form.cleaned_data.get('schedule_type')
        if schedule_type == 'daily':
            habit.days_of_week = [0, 1, 2, 3, 4, 5, 6]
        elif schedule_type == 'weekdays':
            habit.days_of_week = [0, 1, 2, 3, 4]
        elif schedule_type == 'weekends':
            habit.days_of_week = [5, 6]
        else:  
            habit.days_of_week = form.cleaned_data.get('days_of_week', [])
        
        habit.save()
        return habit
    
    @staticmethod
    def update_habit(habit, form):
        habit = form.save(commit=False)
        
        if habit.category == 'other':
            custom_category = form.cleaned_data.get('custom_category')
            if custom_category:
                habit.category = custom_category
        
        schedule_type = form.cleaned_data.get('schedule_type')
        if schedule_type == 'daily':
            habit.days_of_week = [0, 1, 2, 3, 4, 5, 6]
        elif schedule_type == 'weekdays':
            habit.days_of_week = [0, 1, 2, 3, 4]
        elif schedule_type == 'weekends':
            habit.days_of_week = [5, 6]
        else:  
            habit.days_of_week = form.cleaned_data.get('days_of_week', [])
        
        habit.save()
        return habit
    
    @staticmethod
    def delete_habit(habit):
        habit.delete()
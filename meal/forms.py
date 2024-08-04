from django import forms
from .models import Meal

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['user', 'date', 'morning', 'lunch', 'dinner', 'snack']
        widgets = {
            'morning': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'lunch': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'dinner': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'snack': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

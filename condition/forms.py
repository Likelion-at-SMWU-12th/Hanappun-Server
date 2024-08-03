from django import forms
from .models import Condition

class ConditionForm(forms.ModelForm):
    condition_choices = [
        ('두통', '두통'), ('복통', '복통'), ('허리통증', '허리통증'),
        ('변비', '변비'), ('설사', '설사'), ('소화불량', '소화불량'),
        ('메스꺼움/구토', '메스꺼움/구토'), ('근육통', '근육통'), ('발열', '발열'),
        ('오한', '오한'), ('피로 누적', '피로 누적'), ('수면 부족', '수면 부족'),
        ('과호흡', '과호흡'), ('손발저림', '손발저림'), ('어지러움', '어지러움')
    ]

    mood_choices = [
        ('불안/초조', '불안/초조'), ('예민/짜증', '예민/짜증'), 
        ('우울/무기력', '우울/무기력'), ('기억력/집중력 저하', '기억력/집중력 저하'), 
        ('수면장애', '수면장애')
    ]

    condition_cate = forms.MultipleChoiceField(
        choices=condition_choices, widget=forms.CheckboxSelectMultiple, label='몸 상태')
    mood_cate = forms.MultipleChoiceField(
        choices=mood_choices, widget=forms.CheckboxSelectMultiple, label='기분 변화')

    class Meta:
        model = Condition
        fields = ['date', 'condition_cate', 'mood_cate', 'memo']

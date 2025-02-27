from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название задачи',
                                      'style': 'min-width: 150px'}))
    completed = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False, label='Приоритет')
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Описание задачи',
                'style': 'max-height: 150px; min-height: 100px;'
            }
        )
    )
    def clean_title(self):
        title = self.cleaned_data['title']
        if any(char.isdigit() for char in title):  # Проверка на наличие чисел в названии
            raise forms.ValidationError('Название не может содержать цифры')
        return title
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'priority']
        exclude = ['user']

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='Поиск', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_query(self):
        query = self.cleaned_data['query']
        if not query.strip():
            raise forms.ValidationError('Поле поиска не может быть пустым.')
        return query
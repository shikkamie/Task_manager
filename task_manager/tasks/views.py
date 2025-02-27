from logging import raiseExceptions

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from rest_framework import generics

# Create your views here.
from .models import Task
from .forms import TaskForm, SearchForm
from .serializers import TaskSerializer


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    print(f"Пользователь: {request.user}, Количество задач: {tasks.count()}")
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            if 'priority' in form.cleaned_data:
                task.priority = form.cleaned_data['priority']
            task.save()
            return redirect('task_list')
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'form': form})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

@login_required
def search_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            tasks = tasks.filter(title__icontains=query | tasks.filter(description__icontains=query))
    return render(request, 'tasks/search_tasks.html',
                  {'tasks': tasks, 'form': form})

class TaskListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
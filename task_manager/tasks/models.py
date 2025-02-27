from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=12, choices=([('low', 'Низкий'),('medium', 'Средний'),
                                                         ('high', 'Высокий')]), default='medium', blank=True)


    def __str__(self):
        return self.title
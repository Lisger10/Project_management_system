from django.db import models
from tasks.models import Task



ACTIVITIES = [
    ("Проектирование", "Проектирование"),
    ("Разработка", "Разработка"),
    ("Анализ", "Анализ"),
    ("Исправление ошибки", "Исправление ошибки"),
    ("Тестирование", "Тестирование"),
    ("Другое", "Другое"),
]

class Labor(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    activity = models.CharField(max_length=20 ,choices=ACTIVITIES)
    executor = models.CharField(max_length=50, default="user")
    comment = models.CharField(max_length=200)

    class Meta:
        ordering = ['-date']


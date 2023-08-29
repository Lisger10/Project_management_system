from django.db import models
from projects.models import Projects
from django.conf import settings
from django.contrib.auth.models import User


TASK_STATUS = (
    ("Открыта", "Открыта"),
    ("Закрыта", "Закрыта"),
)

TASK_PRIOR = (
    ("Высокий", "Высокий"),
    ("Средний", "Средний"),
    ("Низкий", "Низкий"),
)


class Task(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateField(help_text= '')
    end_date = models.DateField()
    perfomance_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=TASK_PRIOR, default="Низкий")
    status = models.CharField(max_length=10, choices=TASK_STATUS, default= "Открыта")
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    admin = models.CharField(max_length=20, default="user")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Tasks_Users")

    def __str__(self):
        return self.name + ' ' + '(' + self.project.name + ')'

    class Meta:
        ordering = ["-id"]


class Tasks_Users(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, to_field="username", on_delete=models.CASCADE
    )
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE)

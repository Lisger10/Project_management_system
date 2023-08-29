from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


def get_first_name(self):
    return self.first_name + ' ' + self.last_name

User.add_to_class("__str__", get_first_name)


PROJECT_PERFOMANCE = (
    ("Выполнен", "Выполнен"),
    ("Не выполнен", "Не выполнен"),
    ("Отклонен", "Отклонен"),
)


class Projects(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    perfomance_status = models.CharField(
        max_length=15, default="Не выполнен", choices=PROJECT_PERFOMANCE
    )
    perfomance_date = models.DateField(null=True, blank=True)
    admin = models.CharField(max_length=50, default="user")
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Projects_Users"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class Projects_Users(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, to_field="username", on_delete=models.CASCADE
    )
    projects = models.ForeignKey(Projects, on_delete=models.CASCADE)

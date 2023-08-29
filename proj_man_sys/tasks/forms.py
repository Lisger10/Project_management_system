from django import forms
from tasks.models import Task
from django.utils.translation import gettext_lazy as _

class CreateChangeTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ["admin"]
        labels = {
            "name": _("Название"),
            "start_date": _("Дата начала"),
            "end_date": _("Дата завершения"),
            "perfomance_date ": _("Фактическая дата завершения"),
            "status": _("Статус"),
            "priority ": _("Приоритет"),
            "project": _("Проект"),
            "users": _("Пользователи")
        }

        
class ChangeTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        labels = {
            "start_date": _("Дата начала"),
            "end_date": _("Дата завершения"),
            "perfomance_date ": _("Фактическая дата завершения"),
            "status": _("Статус"),
            "priority ": _("Приоритет"),
        }
        exclude = ['name', 'project', 'admin', 'users']

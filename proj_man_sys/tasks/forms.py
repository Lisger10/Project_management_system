from django import forms
from tasks.models import Task
from django.utils.translation import gettext_lazy as _
from .models import Projects
from projects.models import Projects_Users
from django.db.models import Q


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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CreateChangeTaskForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Projects.objects.filter(Q(users= self.request.user.username) | Q(admin = self.request.user.last_name + ' ' + self.request.user.first_name ))
        self.fields['start_date'].widget.attrs['placeholder'] = 'dd.mm.yyyy'
        self.fields['end_date'].widget.attrs['placeholder'] = 'dd.mm.yyyy'
        self.fields['perfomance_date'].widget.attrs['placeholder']= 'dd.mm.yyyy'

        
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

    def __init__(self, *args, **kwargs):
        super(ChangeTaskForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['placeholder'] = 'dd.mm.yyyy'
        self.fields['end_date'].widget.attrs['placeholder'] = 'dd.mm.yyyy'
        self.fields['perfomance_date'].widget.attrs['placeholder']= 'dd.mm.yyyy'
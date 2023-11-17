from django import forms
from labor_costs.models import Labor
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Task
from django.db.models import Q


class CreateLaborForm(forms.ModelForm):
    class Meta:
        model = Labor
        exclude = ["executor"]
        labels = {
            "task": _("Задача"),
            "date": _("Дата"),
            "hours": _("Час(а,ов)"),
            "activity": _("Деятельность"),
            "executor": _("Исполнитель"),
            "comment ": _("Комментарий"),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(CreateLaborForm, self).__init__(*args, **kwargs)
        self.fields["task"].queryset = Task.objects.filter(
            Q(users=self.request.user.username)
            | Q(admin=self.request.user.last_name + " " + self.request.user.first_name)
        )

    def clean_hours(self):
        super().clean()
        hours = self.cleaned_data.get("hours")
        if "." in str(hours):
            minutes = int(str(hours).split(".")[1])
        else:
            minutes = 0
        if hours < 0:
            raise ValidationError("Negative value")
        if minutes>59:
            raise ValidationError("Not correct value")
        return hours

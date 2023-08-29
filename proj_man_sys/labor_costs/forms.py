from django import forms
from labor_costs.models import Labor
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

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



    
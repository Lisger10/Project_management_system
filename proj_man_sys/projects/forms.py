from django import forms
from projects.models import Projects


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        exclude = ["admin"]
    def __init__(self, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['placeholder'] = 'dd.mm.yyyy'
        self.fields['end_date'].widget.attrs['placeholder'] = 'dd.mm.yyyy'
        self.fields['perfomance_date'].widget.attrs['placeholder']= 'dd.mm.yyyy'
    

class ChooseValuesForm(forms.Form):
    MONTH_CHOICES = (('Январь', 'Январь'),
                    ('Февраль', 'Февраль'),
                    ('Март', 'Март'), 
                    ('Апрель', 'Апрель'),
                    ('Май', 'Май'),
                    ('Июнь', 'Июнь'),
                    ('Июль', 'Июль'),
                    ('Август', 'Август'),
                    ('Сентябрь', 'Сентябрь'),
                    ('Октябрь', 'Октябрь'),
                    ('Ноябрь', 'Ноябрь'),
                    ('Декабрь', 'Декабрь'),
                    )
    YEAR_CHOISES = ((2023, 2023),(2024, 2024))
    month = forms.ChoiceField(choices=MONTH_CHOICES, label= 'Месяц')
    year = forms.ChoiceField(choices=YEAR_CHOISES , label = 'Год')
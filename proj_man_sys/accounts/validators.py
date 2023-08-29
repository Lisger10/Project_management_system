from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class MinNumberValidator:
    def validate(self, password1, user=None):
        if len(password1) < 8:
            raise ValidationError(
                _("Длина пароля должна быть не меньше 8 символов"),
                code="password is too short",
            )

    def get_help_text(self):
        return "Пароль не меньше 8 символов"

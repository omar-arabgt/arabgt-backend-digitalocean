from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class CustomAuthenticationForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        if not user.is_active or not user.is_staff:
            raise ValidationError(
                self.error_messages["invalid_login"],
                code="invalid_login",
            )

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


ONE_FIELD_MESSAGE = _("Fill only one field among these")

def check_one_field(model, field1, field2):
    if getattr(model, field1) and getattr(model, field2):
        raise ValidationError(f"{ONE_FIELD_MESSAGE} ({field1}, {field2})")

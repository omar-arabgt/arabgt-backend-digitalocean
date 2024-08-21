from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings

from .choices import MobilePlatform, CAR_SORTING

ONE_FIELD_MESSAGE = _("Fill only one field among these")

def check_one_field(model, field1, field2):
    if getattr(model, field1) and getattr(model, field2):
        raise ValidationError(f"{ONE_FIELD_MESSAGE} ({field1}, {field2})")

def get_detailed_list(keys=None, s3_directory="", list=None):
    if list is None:
        raise ValueError("A list of car brands must be provided.")

    if keys is None:
        keys = [en_label for en_label, _ in list]
    
    return [
        {
            'label': ar_label,
            'value': en_label,
            'image_url': f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_directory}/{en_label.lower()}.png"
        }
        for en_label, ar_label in list if en_label in keys
    ]

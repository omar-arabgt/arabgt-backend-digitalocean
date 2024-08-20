from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .choices import MobilePlatform, CAR_SORTING

ONE_FIELD_MESSAGE = _("Fill only one field among these")

def check_one_field(model, field1, field2):
    if getattr(model, field1) and getattr(model, field2):
        raise ValidationError(f"{ONE_FIELD_MESSAGE} ({field1}, {field2})")

def get_car_sorting_list(keys=None, base_url="https://arabgt-bucket.s3.eu-north-1.amazonaws.com"):
    if keys is None:
        keys = [en_label for en_label, _ in CAR_SORTING]
    
    return [
        {
            'label': ar_label,
            'value': en_label,
            'image_url': f"{base_url}/sort_cars/{en_label}.png"
        }
        for en_label, ar_label in CAR_SORTING if en_label in keys
    ]
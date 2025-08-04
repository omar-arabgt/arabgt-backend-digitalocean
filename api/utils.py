from django.utils.translation import gettext_lazy as _
from django.conf import settings
import re
import phonenumbers

def get_detailed_item_dict_brand(items, s3_directory):
    d = {}
    for en_label, ar_label in items:
        item = {
            "label": ar_label,
            "value": en_label,
            "image_url": f"https://{getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', 'dummy-domain.com')}/{s3_directory}/{en_label}.png"
        }
        d[en_label] = item
    return d

def get_detailed_item_dict(items, s3_directory):
    d = {}
    for en_label, ar_label in items:
        item = {
            "label": ar_label,
            "value": en_label,
            "image_url": f"https://{getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', 'dummy-domain.com')}/{s3_directory}/{en_label.lower()}.png"
        }
        d[en_label] = item
    return d


def subscribe_newsletter(email, unsubscribe=False):
    """
    Subscribes or unsubscribes a user from the newsletter using User model.
    """
    from .models import User
    try:
        user = User.objects.get(email=email, is_staff=False, is_superuser=False)
    except User.DoesNotExist:
        raise Exception("User not found!")

    if unsubscribe:
        if not user.newsletter:
            raise Exception("User is not subscribed!")
        user.newsletter = False
        user.save(update_fields=['newsletter'])
    else:
        if user.newsletter:
            raise Exception("User is already subscribed!")
        user.newsletter = True
        user.save(update_fields=['newsletter'])


def normalize_arabic(text):
    # Remove diacritics and normalize common variations
    text = re.sub(r'[ًٌٍَُِّْـ]', '', text)  # remove tashkeel
    text = re.sub(r'[إأآا]', 'ا', text)     # normalize alef
    return text


def validate_phone_number(phone_data):
    try:
        # Parse the phone number
        phone_obj = phonenumbers.parse(
            phone_data['number'], 
            phone_data['country_code']
        )
        
        # Check if it's a valid number
        if not phonenumbers.is_valid_number(phone_obj):
            return False, "Invalid phone number format"
            
        # Check if it's a possible number
        if not phonenumbers.is_possible_number(phone_obj):
            return False, "Phone number is  wrong"
            
        formatted_number = phonenumbers.format_number(
            phone_obj, 
            phonenumbers.PhoneNumberFormat.E164
        )
        
        return True, formatted_number
        
    except phonenumbers.NumberParseException as e:
        return False, f"Phone number parsing error: {str(e)}"
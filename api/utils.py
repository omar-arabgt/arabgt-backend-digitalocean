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
            "image_url": f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_directory}/{en_label}.png"
        }
        d[en_label] = item
    return d

def get_detailed_item_dict(items, s3_directory):
    d = {}
    for en_label, ar_label in items:
        item = {
            "label": ar_label,
            "value": en_label,
            "image_url": f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_directory}/{en_label.lower()}.png"
        }
        d[en_label] = item
    return d


def subscribe_newsletter(email, unsubscribe=False):
    """
    Subscribes or unsubscribes a user from the newsletter.

    Args:
    - email: The email to subscribe or unsubscribe.
    - unsubscribe: If True, the email is unsubscribed.

    Raises:
    - Exception: If the subscription is not found during unsubscribe or if the email is already subscribed.
    """
    from .models import Newsletter
    from .serializers import NewsletterSerializer

    if unsubscribe:
        try:
            subscription = Newsletter.objects.get(email=email)
        except Newsletter.DoesNotExist:
            raise Exception("Subscription not found!")
        subscription.delete()
    else:
        if Newsletter.objects.filter(email=email).exists():
            raise Exception("Email is already subscribed!")

        serializer = NewsletterSerializer(data={"email": email})
        serializer.is_valid(raise_exception=True)
        serializer.save()


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
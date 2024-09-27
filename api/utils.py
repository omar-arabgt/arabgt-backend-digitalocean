from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings


def get_detailed_list(keys=None, s3_directory="", list=None):
    """
    Generates a detailed list of items, including labels, values, and image URLs.

    Args:
    - keys: Specific keys to include in the list. Defaults to all keys if None.
    - s3_directory: The S3 directory where images are stored.
    - list: A list of tuples containing English and Arabic labels.

    Returns:
    - A list of dictionaries containing 'label', 'value', and 'image_url' for each item.

    Raises:
    - ValueError: If the 'list' argument is not provided.
    """
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

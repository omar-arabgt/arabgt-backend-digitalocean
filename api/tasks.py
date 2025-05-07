from onesignal import ApiClient, Configuration
from onesignal.api import default_api
from onesignal.model.notification import Notification as OneSignalNotification
from twilio.rest import Client
from django.conf import settings
from django.core.cache import cache
from django.db.models import F
from django.db import transaction
from celery import shared_task

from .choices import PointType


NOTIFICATION_ALL = "notification_all"


@shared_task
def send_push_notification(user_id, title, content, link=None, external_link=None, by_admin=False):
    """
    Sends a push notification to a specific user or all users who have notifications enabled.

    Args:
    - user_id: The ID of the user to send the notification to, or NOTIFICATION_ALL for all users.
    - title: The title of the notification.
    - content: The content of the notification.
    - link: An optional link to include with the notification.

    Functionality:
    - Sends the notification through OneSignal and creates a Notification object in the database.
    """
    from .models import User, Notification, AdminNotification

    if user_id == NOTIFICATION_ALL:
        users = User.objects.filter(send_notification=True)
    else:
        users = User.objects.filter(id=user_id, send_notification=True)

    if by_admin:
        AdminNotification.objects.create(
            title=title,
            content=content,
            link=link,
            external_link=external_link,
        )

    if users:
        notifications = []
        for user in users:
            n = Notification(
                user=user,
                title=title,
                content=content,
                link=link,
                external_link=external_link,
                is_admin_notification=by_admin,
            )
        notifications.append(n)

        Notification.objects.bulk_create(notifications)
        users.update(has_notification=True)

        user_ids = users.values_list("id", flat=True)
        user_ids = [str(i) for i in user_ids]

        configuration = Configuration(app_key=settings.ONESIGNAL_API_KEY)
        with ApiClient(configuration) as api_client:
            api_instance = default_api.DefaultApi(api_client)
            notification = OneSignalNotification(
                app_id=settings.ONESIGNAL_APP_ID,
                include_external_user_ids=user_ids,
                contents={"en": content},
                headings={"en": title},
                url=external_link,
                data={"url": link},
                channel_for_external_user_ids="push",
            )
            api_instance.create_notification(notification)


def set_point(user_id, point_type):
    """
    Awards points to a user based on a specific point type.

    Args:
    - user_id: The ID of the user to award points to.
    - point_type: The type of points to award, which must be defined in PointType.

    Functionality:
    - Checks if the user has reached the limit for this point type, and if not, awards the points.
    - Uses a cache to limit the number of points that can be awarded within a certain timeframe.
    """
    point, cache_key, limit, expire = getattr(PointType, point_type).value
    if cache_key and limit and expire:
        KEY = f"{cache_key}:{user_id}"
        count = cache.get_or_set(KEY, 0, 60*60*24*expire)
        if count >= limit:
            return

        client = cache._cache.get_client()
        ttl = client.ttl(cache.make_key(KEY))
        cache.set(KEY, count + 1, ttl)

    with transaction.atomic():
        from .models import User
        user = User.objects.select_for_update().get(id=user_id)
        user.point = F("point") + point
        user.save(update_fields=["point"])


def format_phone_number_for_twilio(phone_number: str) -> str:
    """
    Format a phone number to Twilio-friendly format:
    If it starts with '00', replace it with '++' (double plus).
    
    Args:
        phone_number (str): The original phone number string.
    
    Returns:
        str: The formatted phone number.
    """
    phone_number = phone_number.strip()
    
    if phone_number.startswith('00'):
        return '++' + phone_number[2:]
    return phone_number


@shared_task
def send_sms_notification(phone_number, body):
    """
    Sends an SMS notification to the specified phone number.

    Args:
    - phone_number: The phone number to send the SMS to.
    - body: The content of the SMS.

    Functionality:
    - Uses the Twilio API to send the SMS.
    """
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        from_=settings.TWILIO_FROM_NUMBER,
        to=format_phone_number_for_twilio(phone_number),
        body=body,
    )


@shared_task
def send_otp_code(phone_number: str) -> str:
    """
    Sends an OTP code to the specified phone number using Twilio Verify.

    Returns:
        status (str): Status of the verification attempt (e.g., 'pending')
    """
    ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
    AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
    VERIFY_SERVICE_SID = settings.TWILIO_VERIFY_SERVICE_SID
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    verification = client.verify \
        .v2 \
        .services(VERIFY_SERVICE_SID) \
        .verifications \
        .create(to=format_phone_number_for_twilio(phone_number), channel='sms')
    
    return verification.status

@shared_task
def check_otp_code(phone_number: str, code: str) -> bool:
    """
    Verifies the OTP code for the specified phone number.

    Returns:
        bool: True if verification is approved, False otherwise.
    """
    ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
    AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
    VERIFY_SERVICE_SID = settings.TWILIO_VERIFY_SERVICE_SID

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    verification_check = client.verify \
        .v2 \
        .services(VERIFY_SERVICE_SID) \
        .verification_checks \
        .create(to=format_phone_number_for_twilio(phone_number), code=code)
    
    return verification_check.status == "approved"
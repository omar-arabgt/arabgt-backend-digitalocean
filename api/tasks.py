from onesignal import ApiClient, Configuration
from onesignal.api import default_api
from onesignal.model.notification import Notification as OneSignalNotification
from django.conf import settings
from celery import shared_task

from .models import User, Notification


@shared_task
def send_push_notification(title, content, link=None):
    configuration = Configuration(app_key=settings.ONESIGNAL_API_KEY)
    with ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        notification = OneSignalNotification(
            app_id=settings.ONESIGNAL_APP_ID,
            included_segments=["All"],
            contents={"en": content},
            headings={"en": title},
            url=link,
            channel_for_external_user_ids="push",
        )
        api_instance.create_notification(notification)

    notifications = []
    users = User.objects.all()
    for user in users:
        n = Notification(
            user=user,
            title=title,
            content=content,
            link=link,
            is_admin_notification=True,
        )
        notifications.append(n)
    Notification.objects.bulk_create(notifications)

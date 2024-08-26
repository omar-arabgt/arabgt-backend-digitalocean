from onesignal import ApiClient, Configuration
from onesignal.api import default_api
from onesignal.model.notification import Notification as OneSignalNotification
from django.conf import settings
from celery import shared_task


NOTIFICATION_ALL = "notification_all"


@shared_task
def send_push_notification(user_id, title, content, link=None):
    from .models import User, Notification

    if user_id == NOTIFICATION_ALL:
        user_info = {"included_segments": ["All"]}
    else:
        user_info = {"include_external_user_ids": [str(user_id)]}

    configuration = Configuration(app_key=settings.ONESIGNAL_API_KEY)
    with ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        notification = OneSignalNotification(
            app_id=settings.ONESIGNAL_APP_ID,
            contents={"en": content},
            headings={"en": title},
            url=link,
            channel_for_external_user_ids="push",
            **user_info,
        )
        api_instance.create_notification(notification)

    notifications = []
    if user_id == NOTIFICATION_ALL:
        users = User.objects.all()
    else:
        users = User.objects.filter(id=user_id)

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

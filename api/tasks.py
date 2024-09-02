from onesignal import ApiClient, Configuration
from onesignal.api import default_api
from onesignal.model.notification import Notification as OneSignalNotification
from django.conf import settings
from django.core.cache import cache
from django.db.models import F
from django.db import transaction
from celery import shared_task

from .choices import PointType


NOTIFICATION_ALL = "notification_all"


@shared_task
def send_push_notification(user_id, title, content, link=None):
    from .models import User, Notification

    if user_id == NOTIFICATION_ALL:
        users = User.objects.filter(send_notification=True)
    else:
        users = User.objects.filter(id=user_id, send_notification=True)

    if users:
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
                url=link,
                channel_for_external_user_ids="push",
            )
            api_instance.create_notification(notification)

        notifications = []
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


@shared_task
def set_point(user_id, point_type):
    point, cache_key, limit, expire = getattr(PointType, point_type).value
    if cache_key and limit and expire:
        KEY = f"{cache_key}:{user_id}"
        count = cache.get_or_set(KEY, 0, 60*60*expire)
        if count >= limit:
            return
        cache.set(KEY, count + 1)

    with transaction.atomic():
        from .models import User
        user = User.objects.select_for_update().get(id=user_id)
        user.point = F("point") + point
        user.save(update_fields=["point"])

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import gettext_lazy as _


from .models import GroupMembership, Question, Reply, Reaction
from .choices import PointType
from .tasks import set_point, send_push_notification


@receiver(post_save, sender=GroupMembership) 
def post_save_groupmembership(sender, instance, created, **kwargs):
    if created:
        set_point(instance.user_id, PointType.GROUP_MEMBERSHIP.name)


@receiver(post_save, sender=Question) 
def post_save_question(sender, instance, created, **kwargs):
    if created:
        set_point(instance.user_id, PointType.QUESTION.name)


@receiver(post_save, sender=Reply) 
def post_save_reply(sender, instance, created, **kwargs):
    if created:
        if instance.question:
            model = instance.question
            question_id = model.id
            message = _("commented on your post")
        else:
            model = instance.parent_reply
            question_id = model.question.id
            message = _("replied your comment")

        content = f"{instance.user.first_name} {message}: {instance.content}"
        link = f"{settings.APP_URL}/question-details?id={question_id}"
        send_push_notification.delay(model.user_id, None, content, link)
        set_point(instance.user_id, PointType.REPLY.name)


@receiver(post_save, sender=Reaction) 
def post_save_reaction(sender, instance, created, **kwargs):
    if created:
        set_point(instance.user_id, PointType.REACTION.name)

        model = instance.content_type.model
        obj = instance.content_object
        message = None
        if model == "question":
            message = _("liked your post")
            question_id = obj.id
        elif model == "reply":
            message = _("liked your comment")
            if obj.question:
                question_id = obj.question.id
            else:
                question_id = obj.parent_reply.question.id

        if message:
            link = f"{settings.APP_URL}/question-details?id={question_id}"
            content = f"{instance.user.first_name} {message}: {obj.content}"
            send_push_notification.delay(obj.user_id, None, content, link)

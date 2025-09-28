from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from login_registration_app.models import Attachment

channel_layer = get_channel_layer()

@receiver(post_save, sender=Attachment)
def broadcast_attachment_status(sender, instance, **kwargs):
    case = instance.case
    async_to_sync(channel_layer.group_send)(
        f"case_{case.id}",
        {
            "type": "status.update",
            "payload": {
                "status": case.status,
                "attachments": list(case.case_attachments.values("id", "status"))
            }
        }
    )

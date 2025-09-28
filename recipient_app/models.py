from django.db.models.signals import post_save
from django.dispatch import receiver

from login_registration_app.models import Attachment
from .models import *

@receiver(post_save, sender=Attachment)
def update_case_status_on_attachment(sender, instance, **kwargs):
    case = instance.case
    attachments = case.case_attachments.all()

    if attachments.filter(status="approved").exists():
        case.status = "approved"
    elif attachments.exists() and not attachments.exclude(status="rejected").exists():
        case.status = "rejected"
    else:
        case.status = "pending"

    case.save(update_fields=["status"])
    print(f"Case {case.id} updated → {case.status}")

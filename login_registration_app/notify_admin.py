# login_registration_app/notify_admin.py
from django.core.mail import send_mail
from smtplib import SMTPException
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def notify_admin_new_case(case):
    subject = f"New Case #{case.id} with Attachment Needs Verification"
    admin_url = reverse(f"admin:{case._meta.app_label}_{case._meta.model_name}_change", args=[case.pk])
    full_url = f"http://127.0.0.1:8000/admin" 

    message = (
        f"A new case has been submitted and requires verification.\n\n"
        f"Case ID: {case.id}\n"
        f"Description: {case.description}\n"
        f"Price: ${case.price}\n\n"
        f"Open in Admin: {full_url}\n"
    )

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        logger.info("Admin notification sent for case %s", case.id)
    except SMTPException as e:
        logger.exception("❌ Failed to send admin email for case %s: %s", case.id, e)

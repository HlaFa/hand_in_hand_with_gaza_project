from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import User, Case, Adoption, Attachment, Category


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "case", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    actions = ["approve_attachments", "reject_attachments"]

    def send_ws_update(self, case):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"case_{case.id}",
            {
                "type": "status.update",
                "status": case.status,
                "attachments": list(case.case_attachments.values("id", "status")),
            }
        )

    def approve_attachments(self, request, queryset):
        updated = 0
        for att in queryset:
            att.status = "approved"
            att.save()
            case = att.case
            if case.status.lower() == "pending":
                case.status = "approved"
                case.save()
            self.send_ws_update(case)
            updated += 1
        self.message_user(request, f"{updated} attachments approved ✅")

    def reject_attachments(self, request, queryset):
        updated = 0
        for att in queryset:
            att.status = "rejected"
            att.save()
            self.send_ws_update(att.case)
            updated += 1
        self.message_user(request, f"{updated} attachments rejected ❌")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.status == "pending":
            send_mail(
                "New Proof Submitted",
                f"A new attachment for case {obj.case.id} has been submitted by {obj.user.first_name}.",
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
            )
            self.send_ws_update(obj.case)

admin.site.register(User)
admin.site.register(Case)
admin.site.register(Adoption)
admin.site.register(Category)
admin.site.register(Attachment, AttachmentAdmin)


def update_case_status(case):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"case_{case.id}",
        {
            "type": "case_status",
            "status": case.status,
        }
    )
from django import forms

from login_registration_app.models import Attachment, Case
from .models import *

class CaseForm(forms.ModelForm):
    attachment = forms.FileField(required=True)

    class Meta:
        model = Case
        fields = ['description', 'price', 'category']

    def save_attachment(self, user, case):
        file = self.cleaned_data['attachment']
        Attachment.objects.create(
            case=case,
            user=user,
            file_path=file,
            status='pending'
        )

from django import forms
from login_registration_app.models import Attachment, Case

class CaseForm(forms.ModelForm):
    attachment = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control shadow-sm",
                "accept": ".jpg,.jpeg,.png,.pdf",  
            }
        )
    )

    class Meta:
        model = Case
        fields = ["description", "price", "category"]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "form-control rounded-3 shadow-sm",
                    "rows": 4,
                    "placeholder": "Describe the case clearly (e.g., medical, food, shelter)...",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control rounded-3 shadow-sm",
                    "min": "1",
                    "placeholder": "Enter amount in USD",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select rounded-3 shadow-sm",
                }
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "Choose a category..."
    def save(self, user=None, commit=True):
        case = super().save(commit=False)
        if user:
            case.user = user
        if commit:
            case.save()
            file = self.cleaned_data.get("attachment")
            if file:
                Attachment.objects.create(
                    case=case,
                    user=user,
                    file=file,
                    status="pending",
                )
        return case
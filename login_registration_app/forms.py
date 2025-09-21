from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from datetime import date
from .models import User
import re

# ////////////////////////////regex email validation ////////////////////////////
def validate_custom_email(value):
    pattern = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
    if not re.match(pattern, value):
        raise ValidationError("The email is not valid")

# ////////////////////////////register validation ////////////////////////////
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        min_length=8
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        error_messages={'required': 'This field is required.'}
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        validators=[validate_custom_email]
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'link_watsapp', 'dob', 'phone',
            'role', 'national_id', 'email', 'password'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'link_watsapp': forms.URLInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # ////////////////////////////email validation ////////////////////////////
    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    # ////////////////////////////ID validation ////////////////////////////
    def clean_national_id(self):
        national_id = self.cleaned_data.get("national_id", "").strip()
        if not re.match(r'^\d{9}$', national_id):
            raise ValidationError("National ID must be exactly 9 digits.")
        return national_id

    # ////////////////////////////dob validation ////////////////////////////
    def clean_dob(self):
        dob = self.cleaned_data.get("dob")
        if not dob:
            return dob

        today = date.today()
        if dob > today:
            raise ValidationError("Date of birth cannot be in the future.")

 
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 12:
            raise ValidationError("You must be at least 12 years old to register.")
        return dob

    # ////////////////////////////password validation ////////////////////////////
    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        confirm = cleaned.get("confirm_password")
        if pwd and confirm and pwd != confirm:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password']) 
        if commit:
            user.save()
        return user

    # ////////////////////////////login validation ////////////////////////////
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    def clean(self):
        cleaned = super().clean()
        cleaned['email'] = (cleaned.get('email') or '').strip().lower()
        cleaned['password'] = (cleaned.get('password') or '').strip()
        return cleaned
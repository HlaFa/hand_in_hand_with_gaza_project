from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib import admin
from .models import User, Category, Case, Adoption, Attachment

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Case)
admin.site.register(Adoption)
admin.site.register(Attachment)

# class UserAdminForm(forms.ModelForm):
#     def clean_password(self):
#         password = self.cleaned_data['password']
#         if not password.startswith("pbkdf2_sha256$"):
#             return make_password(password)
#         return password

#     class Meta:
#         model = User
#         fields = '__all__'


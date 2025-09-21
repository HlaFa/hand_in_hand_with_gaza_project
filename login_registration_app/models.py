from django.db import models
 
# -------------------------
# Users
# -------------------------
class User(models.Model):
    ROLE_CHOICES = (
        ('donor', 'Donor'),
        ('recipient', 'Recipient'),
    )
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    link_watsapp = models.URLField()
    dob = models.DateField()
    phone = models.BigIntegerField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='recipient')
    national_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}"
 
# -------------------------
# Categories
# -------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateField()
    updated_at = models.DateField()
 
    def __str__(self):
        return self.name
 
# -------------------------
# Cases
# -------------------------
class Case(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('Approved', 'Approved'),
        ('delivered', 'Delivered'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="category_cases")
 
    def __str__(self):
        return f"Case {self.id} - {self.status}"
 
# -------------------------
# Adoptions
# -------------------------
class Adoption(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    case = models.ForeignKey(Case, on_delete=models.CASCADE,related_name="case_adoptions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
 
    def __str__(self):
        return f"Adoption {self.id} by {self.donor.first_name}"
 
# -------------------------
# Attachments
# -------------------------
class Attachment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    case = models.ForeignKey(Case, on_delete=models.CASCADE,related_name="case_attachments")
    file_path = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_attachments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return f"Attachment {self.id} for Case {self.case.id}"
from django.db import models

# Create your models here.
class Contact(models.Model):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    linked_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='linked_contacts')
    link_precedence = models.CharField(max_length=10, choices=[('primary', 'Primary'), ('secondary', 'Secondary')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.email or self.phone_number}"
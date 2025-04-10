from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


class GeneratedDocument(models.Model):
    DOCUMENT_TYPES = [
        ('acts', 'Акты'),
        ('orders', 'Приказы'),
        ('document_package', 'Пакет документов')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    organization_name = models.CharField(max_length=255)
    inn = models.CharField(max_length=12)
    ogrn = models.CharField(max_length=13)
    address = models.CharField(max_length=255, default="Не указано")
    responsible_person = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} for {self.organization_name} by {self.user.username}"


class DocumentTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template_name = models.CharField(max_length=255)
    template_file = models.FileField(upload_to='templates/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.template_name
from django.db import models
from django_tenants.models import DomainMixin, TenantMixin
from easy_thumbnails.fields import ThumbnailerImageField


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    additional_info = models.JSONField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name

def content_file_name(instance, filename):
    return f"client_{instance.client.id}/logo/{filename}"


def content_cover_name(instance, filename):
    return f"client_{instance.client.id}/cover_photo/{filename}"


class ClientDetails(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name="details")
    slogan = models.TextField(blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)
    logo = ThumbnailerImageField(
        'ClientLogo',
        upload_to=content_file_name,
        blank=True,
        null=True
    )
    cover_photo = ThumbnailerImageField(
        'ClientCoverPhoto',
        upload_to=content_cover_name,
        blank=True,
        null=True
    )
    logo_url = models.TextField(
        blank=True,
        null=True
    )
    cover_photo_url = models.TextField(
        blank=True,
        null=True
    )
    address = models.TextField(blank=True, null=True)
    formation_date = models.DateField(blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    fcm_url = models.URLField(default="https://fcm.googleapis.com/fcm/send")
    fcm_config = models.JSONField(blank=True, null=True)
    fcm_key = models.TextField(blank=True, null=True)

    # default permissions
    user_device_limit_restriction = models.BooleanField(default=False)
    user_device_recognition_restriction = models.BooleanField(default=False)
    approval_needed_for_allowed_devices = models.BooleanField(default=False)
    user_login_allowed_from_multiple_device = models.BooleanField(default=True)


class Domain(DomainMixin):
    pass

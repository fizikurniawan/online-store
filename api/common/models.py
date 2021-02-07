import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

BASE_URL = getattr(settings, 'BASE_URL')


class BaseModelGeneric(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(db_index=True)
    updated_at = models.DateTimeField(db_index=True, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        now = timezone.now()

        if self.created_at is None:
            self.created_at = now

        # always update
        self.updated_at = now

        return super(BaseModelGeneric, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()

        return super(BaseModelGeneric, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class File(BaseModelGeneric):
    display_name = models.CharField(max_length=150)
    short_name = models.SlugField(max_length=150, blank=True, null=True)
    file = models.FileField(
        max_length=300,
        blank=True,
        null=True
    )
    description = models.TextField(blank=True, null=True)

    def get_url(self):
        if self.file and self.file.url:
            return BASE_URL+'/static/upload' + self.file.url
        return None

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")

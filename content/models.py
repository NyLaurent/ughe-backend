from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=160, default="University of Global Health Equity")
    logo = models.ImageField(upload_to="site/", blank=True)
    logo_url = models.CharField(
        max_length=500, blank=True, help_text="Optional URL or frontend public asset path."
    )
    facts_eyebrow = models.CharField(max_length=100, default="Our impact")
    facts_title = models.CharField(max_length=160, default="Facts & Stats")

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError("Only one set of site settings can be published.")
        return super().save(*args, **kwargs)


class NavigationItem(models.Model):
    class Placement(models.TextChoices):
        PRIMARY = "primary", "Primary navigation"
        HEADER = "header", "Header action"

    class Kind(models.TextChoices):
        LINK = "link", "Link"
        SEARCH = "search", "Search button"
        ADMIN_LOGIN = "admin_login", "Staff login"

    label = models.CharField(max_length=80)
    url = models.CharField(max_length=500)
    placement = models.CharField(max_length=12, choices=Placement.choices, default=Placement.PRIMARY)
    kind = models.CharField(max_length=12, choices=Kind.choices, default=Kind.LINK)
    show_dropdown = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Navigation item"
        verbose_name_plural = "Navigation items"

    def __str__(self):
        return self.label


class Slide(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"

    eyebrow = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=240)
    description = models.TextField(blank=True)
    button_label = models.CharField(max_length=80, blank=True)
    button_url = models.CharField(max_length=500, blank=True)
    media_type = models.CharField(max_length=8, choices=MediaType.choices, default=MediaType.IMAGE)
    media_file = models.FileField(upload_to="slides/", blank=True)
    media_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="Use an absolute URL or a frontend public asset path if no file is uploaded.",
    )
    alt_text = models.CharField(max_length=240, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if not self.media_file and not self.media_url:
            raise ValidationError("Upload a media file or provide a media URL.")
        if self.media_file:
            extension = Path(self.media_file.name).suffix.lower()
            allowed_extensions = {
                self.MediaType.IMAGE: {".jpg", ".jpeg", ".png", ".gif", ".webp"},
                self.MediaType.VIDEO: {".mp4", ".webm", ".ogv", ".ogg"},
            }
            if extension not in allowed_extensions[self.media_type]:
                raise ValidationError(
                    {"media_file": f"Choose a supported {self.media_type} file."}
                )


class StatItem(models.Model):
    value = models.CharField(max_length=40)
    description = models.CharField(max_length=300)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Fact and statistic"
        verbose_name_plural = "Facts and statistics"

    def __str__(self):
        return f"{self.value}: {self.description[:60]}"

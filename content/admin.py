from django.contrib import admin
from .models import NavigationItem, SiteSettings, Slide, StatItem


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Branding", {"fields": ("site_name", "logo", "logo_url")}),
        ("Facts section", {"fields": ("facts_eyebrow", "facts_title")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists() and super().has_add_permission(request)


@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ("label", "placement", "kind", "url", "sort_order", "is_active")
    list_filter = ("placement", "kind", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("label", "url")
    ordering = ("placement", "sort_order")


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "sort_order", "is_active")
    list_filter = ("media_type", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("title", "eyebrow", "description")
    ordering = ("sort_order",)
    fieldsets = (
        ("Slide content", {"fields": ("eyebrow", "title", "description", "button_label", "button_url", "alt_text")}),
        ("Media", {"fields": ("media_type", "media_file", "media_url")}),
        ("Publishing", {"fields": ("sort_order", "is_active")}),
    )


@admin.register(StatItem)
class StatItemAdmin(admin.ModelAdmin):
    list_display = ("value", "description", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("value", "description")
    ordering = ("sort_order",)

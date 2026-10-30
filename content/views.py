from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NavigationItem, SiteSettings, Slide, StatItem


class HomeContentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        settings = SiteSettings.objects.first()
        header_items = NavigationItem.objects.filter(
            placement=NavigationItem.Placement.HEADER, is_active=True
        )
        navigation_items = NavigationItem.objects.filter(
            placement=NavigationItem.Placement.PRIMARY, is_active=True
        )
        slides = Slide.objects.filter(is_active=True)
        stats = StatItem.objects.filter(is_active=True)

        return Response(
            {
                "site": {
                    "name": settings.site_name if settings else "",
                    "logo_url": self._file_or_url(request, settings.logo, settings.logo_url)
                    if settings
                    else "",
                    "facts_eyebrow": settings.facts_eyebrow if settings else "",
                    "facts_title": settings.facts_title if settings else "",
                    "admin_url": request.build_absolute_uri("/admin/"),
                },
                "header_actions": [
                    {
                        "label": item.label,
                        "url": request.build_absolute_uri("/admin/")
                        if item.kind == NavigationItem.Kind.ADMIN_LOGIN
                        else item.url,
                        "kind": item.kind,
                    }
                    for item in header_items
                ],
                "navigation": [
                    {
                        "label": item.label,
                        "url": item.url,
                        "show_dropdown": item.show_dropdown,
                    }
                    for item in navigation_items
                ],
                "slides": [
                    {
                        "eyebrow": slide.eyebrow,
                        "title": slide.title,
                        "description": slide.description,
                        "button_label": slide.button_label,
                        "button_url": slide.button_url,
                        "media_type": slide.media_type,
                        "media_url": self._file_or_url(request, slide.media_file, slide.media_url),
                        "alt_text": slide.alt_text,
                    }
                    for slide in slides
                ],
                "stats": [
                    {"value": stat.value, "description": stat.description}
                    for stat in stats
                ],
            }
        )

    @staticmethod
    def _file_or_url(request, file_field, url):
        if file_field:
            return request.build_absolute_uri(file_field.url)
        return url

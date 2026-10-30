from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test import override_settings
from rest_framework.test import APIClient
from tempfile import TemporaryDirectory

from .models import NavigationItem, SiteSettings, Slide, StatItem


class HomeContentApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_homepage_returns_active_admin_managed_content(self):
        SiteSettings.objects.create(
            site_name="UGHE Test Web App",
            logo_url="/assets/ughe-logo.png",
            facts_title="Community impact",
        )
        NavigationItem.objects.create(label="About", url="#about")
        NavigationItem.objects.create(label="Hidden", url="#hidden", is_active=False)
        NavigationItem.objects.create(
            label="Staff login",
            url="/admin/",
            placement=NavigationItem.Placement.HEADER,
            kind=NavigationItem.Kind.ADMIN_LOGIN,
        )
        Slide.objects.create(title="Welcome", media_url="/assets/slide.jpg")
        Slide.objects.create(title="Draft", media_url="/assets/draft.jpg", is_active=False)
        StatItem.objects.create(value="128", description="People trained")

        response = self.client.get("/api/home/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["site"]["name"], "UGHE Test Web App")
        self.assertEqual(response.data["site"]["facts_title"], "Community impact")
        self.assertEqual([item["label"] for item in response.data["navigation"]], ["About"])
        self.assertEqual(response.data["header_actions"][0]["url"], "http://testserver/admin/")
        self.assertEqual([item["title"] for item in response.data["slides"]], ["Welcome"])
        self.assertEqual(response.data["slides"][0]["media_url"], "/assets/slide.jpg")
        self.assertEqual([item["value"] for item in response.data["stats"]], ["128"])

    def test_uploaded_media_urls_are_absolute(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                Slide.objects.create(
                    title="Uploaded",
                    media_file=SimpleUploadedFile(
                        "slide.mp4", b"video-data", content_type="video/mp4"
                    ),
                    media_type=Slide.MediaType.VIDEO,
                )

                response = self.client.get("/api/home/")

                self.assertEqual(response.status_code, 200)
                self.assertIn("/media/slides/", response.data["slides"][0]["media_url"])
                self.assertTrue(response.data["slides"][0]["media_url"].endswith(".mp4"))

    def test_slide_rejects_media_extension_for_wrong_type(self):
        slide = Slide(
            title="Invalid media",
            media_file="slides/slide.mp4",
            media_type=Slide.MediaType.IMAGE,
        )

        with self.assertRaisesMessage(ValidationError, "Choose a supported image file."):
            slide.full_clean()


class AdminLoginTests(TestCase):
    def test_staff_user_can_log_in_to_django_admin(self):
        user = get_user_model().objects.create_superuser(
            username="content-editor", email="editor@example.org", password="safe-test-password"
        )

        response = self.client.post(
            "/admin/login/",
            {"username": user.username, "password": "safe-test-password", "next": "/admin/"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/admin/"), response.url)

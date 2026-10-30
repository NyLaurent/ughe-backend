import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the initial Django admin user from environment credentials."

    def handle(self, *args, **options):
        username = os.environ.get("UGHE_ADMIN_USERNAME", "").strip()
        password = os.environ.get("UGHE_ADMIN_PASSWORD", "")
        if not username or not password:
            raise CommandError(
                "Set UGHE_ADMIN_USERNAME and UGHE_ADMIN_PASSWORD before creating the admin user."
            )

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={"is_staff": True, "is_superuser": True, "is_active": True},
        )
        if created:
            user.set_password(password)
            user.save(update_fields=["password"])
            self.stdout.write(self.style.SUCCESS(f"Created admin user '{username}'."))
        elif not user.is_staff or not user.is_superuser:
            raise CommandError(
                f"User '{username}' already exists but is not a superuser; choose a different username."
            )
        else:
            self.stdout.write(f"Admin user '{username}' already exists; password was not changed.")

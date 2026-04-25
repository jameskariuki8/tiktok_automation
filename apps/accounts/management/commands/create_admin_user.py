from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Create the default admin user (id=1) if it does not already exist."

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM accounts_user WHERE id = 1")
            row = cursor.fetchone()

        if row:
            self.stdout.write(
                self.style.WARNING("Admin user with id=1 already exists — skipping.")
            )
            return

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO accounts_user (
                    id,
                    username,
                    password,
                    is_superuser,
                    is_staff,
                    is_active,
                    first_name,
                    last_name,
                    email,
                    date_joined,
                    tiktok_account_id,
                    tiktok_access_token,
                    tiktok_refresh_token,
                    is_tiktok_connected,
                    ai_credits,
                    created_at,
                    updated_at
                ) VALUES (
                    1,
                    'admin',
                    'pbkdf2_sha256$600000$t7x8FqH8B9p2$O7vJjR7f+E9k4zLd9jQ7p6vVjP8=',
                    TRUE,
                    TRUE,
                    TRUE,
                    'Admin',
                    'User',
                    'admin@example.com',
                    NOW(),
                    NULL,
                    NULL,
                    NULL,
                    FALSE,
                    100,
                    NOW(),
                    NOW()
                )
                """
            )

        self.stdout.write(
            self.style.SUCCESS("Admin user (id=1) created successfully.")
        )

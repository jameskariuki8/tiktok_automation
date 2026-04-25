import sys
import traceback

from django.core.management.base import BaseCommand
from django.db import connection, OperationalError, ProgrammingError


class Command(BaseCommand):
    help = "Create the default admin user (id=1) if it does not already exist."

    def handle(self, *args, **options):
        self.stdout.write("=== create_admin_user: starting ===")
        self.stdout.flush()

        # ------------------------------------------------------------------ #
        # 1. Verify the database connection is reachable                      #
        # ------------------------------------------------------------------ #
        self.stdout.write("Verifying database connection...")
        self.stdout.flush()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
            self.stdout.write(self.style.SUCCESS(f"  Database connection OK (SELECT 1 => {result})"))
        except (OperationalError, ProgrammingError) as exc:
            self.stderr.write(self.style.ERROR(f"  Database connection FAILED: {exc}"))
            self.stderr.write(traceback.format_exc())
            sys.exit(1)

        # ------------------------------------------------------------------ #
        # 2. Check whether the admin user already exists                      #
        # ------------------------------------------------------------------ #
        check_sql = "SELECT id, username FROM accounts_user WHERE id = 1"
        self.stdout.write(f"Checking for existing admin user — SQL: {check_sql}")
        self.stdout.flush()
        try:
            with connection.cursor() as cursor:
                cursor.execute(check_sql)
                row = cursor.fetchone()
        except (OperationalError, ProgrammingError) as exc:
            self.stderr.write(self.style.ERROR(f"  SELECT failed: {exc}"))
            self.stderr.write(traceback.format_exc())
            sys.exit(1)

        if row:
            self.stdout.write(
                self.style.WARNING(f"  Admin user already exists (id={row[0]}, username={row[1]}) — skipping.")
            )
            return

        self.stdout.write("  No existing admin user found — proceeding with INSERT.")

        # ------------------------------------------------------------------ #
        # 3. Insert the admin user                                            #
        # ------------------------------------------------------------------ #
        insert_sql = """
            INSERT INTO accounts_user (
                username,
                password,
                is_superuser,
                is_staff,
                is_active,
                first_name,
                last_name,
                email,
                date_joined,
                last_login,
                tiktok_account_id,
                tiktok_access_token,
                tiktok_refresh_token,
                is_tiktok_connected,
                ai_credits,
                created_at,
                updated_at
            ) VALUES (
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
                NULL,
                FALSE,
                100,
                NOW(),
                NOW()
            )
        """
        self.stdout.write(f"Executing INSERT — SQL:{insert_sql}")
        self.stdout.flush()
        try:
            with connection.cursor() as cursor:
                cursor.execute(insert_sql)
                row_count = cursor.rowcount
            self.stdout.write(f"  INSERT executed — rows affected: {row_count}")
        except (OperationalError, ProgrammingError) as exc:
            self.stderr.write(self.style.ERROR(f"  INSERT failed: {exc}"))
            self.stderr.write(traceback.format_exc())
            sys.exit(1)
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"  Unexpected error during INSERT: {exc}"))
            self.stderr.write(traceback.format_exc())
            sys.exit(1)

        # ------------------------------------------------------------------ #
        # 4. Confirm the row is now present                                   #
        # ------------------------------------------------------------------ #
        verify_sql = "SELECT id, username, is_superuser, is_staff FROM accounts_user WHERE username = 'admin'"
        self.stdout.write(f"Verifying INSERT — SQL: {verify_sql}")
        self.stdout.flush()
        try:
            with connection.cursor() as cursor:
                cursor.execute(verify_sql)
                created = cursor.fetchone()
        except (OperationalError, ProgrammingError) as exc:
            self.stderr.write(self.style.ERROR(f"  Verification SELECT failed: {exc}"))
            self.stderr.write(traceback.format_exc())
            sys.exit(1)

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"  Admin user created and verified — "
                    f"id={created[0]}, username={created[1]}, "
                    f"is_superuser={created[2]}, is_staff={created[3]}"
                )
            )
        else:
            self.stderr.write(
                self.style.ERROR(
                    "  INSERT reported success but the row is NOT visible in a follow-up SELECT. "
                    "This may indicate a transaction/autocommit issue."
                )
            )
            sys.exit(1)

        self.stdout.write("=== create_admin_user: done ===")
        self.stdout.flush()

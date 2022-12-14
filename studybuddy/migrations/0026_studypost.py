# Generated by Django 4.1.1 on 2022-11-07 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("studybuddy", "0025_mnemonics"),
    ]

    operations = [
        migrations.CreateModel(
            name="StudyPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timeDate", models.DateTimeField(default=django.utils.timezone.now)),
                ("location", models.CharField(max_length=200)),
                ("description", models.TextField(default="", max_length=500)),
                (
                    "groupUsers",
                    models.ManyToManyField(
                        related_name="other_users_joining", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "requests",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users_want_to_join",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("studyClass", models.ManyToManyField(to="studybuddy.scheduleclass")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

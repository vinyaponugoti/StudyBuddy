# Generated by Django 4.1.1 on 2022-11-11 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("studybuddy", "0034_remove_studypost_studyclass_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PostRequest",
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
                ("is_accepted", models.BooleanField(default=False)),
                (
                    "buddy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="buddy",
                        to="studybuddy.profile",
                    ),
                ),
                (
                    "studyposting",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="studypost",
                        to="studybuddy.studypost",
                    ),
                ),
            ],
        ),
    ]

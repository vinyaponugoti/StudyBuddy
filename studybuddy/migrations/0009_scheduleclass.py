# Generated by Django 4.1.1 on 2022-11-05 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("studybuddy", "0008_studypost"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScheduleClass",
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
                ("class_department", models.TextField(blank=True)),
                ("class_number", models.IntegerField(blank=True)),
            ],
        ),
    ]

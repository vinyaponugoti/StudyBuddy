# Generated by Django 4.1.1 on 2022-11-07 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("studybuddy", "0024_delete_mnemonics"),
    ]

    operations = [
        migrations.CreateModel(
            name="Mnemonics",
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
                ("course_mnemonics", models.CharField(max_length=5)),
            ],
        ),
    ]

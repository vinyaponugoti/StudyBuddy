# Generated by Django 4.1.1 on 2022-11-05 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("studybuddy", "0011_remove_profile_schedule"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="schedule",
            field=models.ManyToManyField(
                blank=True, related_name="schedule", to="studybuddy.lutherclass"
            ),
        ),
    ]

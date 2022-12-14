# Generated by Django 4.1.1 on 2022-11-05 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("studybuddy", "0019_remove_scheduleclass_classes_owner"),
    ]

    operations = [
        migrations.AddField(
            model_name="scheduleclass",
            name="classes_owner",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="classes_owner",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

# Generated by Django 4.2.dev20220603193729 on 2022-11-21 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("studybuddy", "0035_postrequest"),
    ]

    operations = [
        migrations.AddField(
            model_name="studypost",
            name="session",
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.1.1 on 2022-11-09 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("studybuddy", "0030_studypost"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studypost",
            name="user_class",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_class",
                to="studybuddy.scheduleclass",
            ),
        ),
    ]

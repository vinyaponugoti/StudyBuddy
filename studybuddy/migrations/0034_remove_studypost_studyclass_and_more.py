# Generated by Django 4.1.1 on 2022-11-09 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("studybuddy", "0033_studypost_user_luther_class"),
    ]

    operations = [
        migrations.RemoveField(model_name="studypost", name="studyClass",),
        migrations.RemoveField(model_name="studypost", name="user_class",),
    ]
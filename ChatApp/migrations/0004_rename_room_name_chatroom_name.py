# Generated by Django 4.1.1 on 2022-11-27 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0003_chat_delete_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatroom',
            old_name='room_name',
            new_name='name',
        ),
    ]

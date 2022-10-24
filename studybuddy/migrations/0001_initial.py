# Generated by Django 4.1.1 on 2022-10-24 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_mnemonic', models.CharField(max_length=5)),
                ('course_number', models.CharField(max_length=5)),
                ('other_info', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Mnemonics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_mnemonics', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='SISClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DeptNnemonic', models.TextField()),
                ('DeptName', models.TextField()),
                ('CourseNumber', models.IntegerField()),
                ('SectionNumber', models.IntegerField()),
                ('ClassName', models.TextField()),
                ('SectionName', models.TextField()),
                ('ProfessorName', models.TextField()),
                ('ProfessorEmail', models.TextField()),
                ('AvailableSeats', models.IntegerField()),
                ('DaysOfTheWeek', models.TextField()),
                ('Semester', models.TextField()),
            ],
        ),
    ]

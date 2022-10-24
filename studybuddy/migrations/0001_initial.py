# Generated by Django 4.1.1 on 2022-10-24 04:35

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
            name='LutherClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DeptNnemonic', models.CharField(max_length=50)),
                ('DeptName', models.CharField(max_length=50)),
                ('CourseNumber', models.CharField(max_length=50)),
                ('SectionNumber', models.CharField(max_length=50)),
                ('ClassName', models.CharField(max_length=50)),
                ('SectionName', models.CharField(max_length=50)),
                ('ProfessorName', models.CharField(max_length=50)),
                ('ProfessorEmail', models.CharField(max_length=50)),
                ('AvailableSeats', models.CharField(max_length=50)),
                ('DaysOfTheWeek', models.CharField(max_length=50)),
                ('Semester', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Mnemonics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_mnemonics', models.CharField(max_length=5)),
            ],
        ),
    ]

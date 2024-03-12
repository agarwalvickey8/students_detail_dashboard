# Generated by Django 5.0.2 on 2024-03-01 09:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffsignup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='staff',
            old_name='password',
            new_name='Password',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='username',
        ),
        migrations.AddField(
            model_name='staff',
            name='Name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='staff',
            name='Branch',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='staffsignup.branch'),
        ),
        migrations.CreateModel(
            name='StudentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CoachingRegisteration', models.CharField(max_length=100)),
                ('CoachingRoll', models.CharField(max_length=100)),
                ('Name', models.CharField(max_length=100)),
                ('FatherName', models.CharField(max_length=100)),
                ('MotherName', models.CharField(max_length=100)),
                ('Course', models.CharField(max_length=100)),
                ('CourseId', models.IntegerField()),
                ('Batch', models.CharField(max_length=100)),
                ('Medium', models.CharField(max_length=100)),
                ('DOB', models.DateField()),
                ('Gender', models.CharField(max_length=100)),
                ('Category', models.CharField(max_length=100)),
                ('Address', models.CharField(max_length=500)),
                ('Tehsil', models.CharField(max_length=100)),
                ('District', models.CharField(max_length=100)),
                ('State', models.CharField(max_length=100)),
                ('PreviousRoll', models.CharField(max_length=100)),
                ('CourseType', models.CharField(max_length=100)),
                ('Branch', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='staffsignup.branch')),
            ],
        ),
    ]

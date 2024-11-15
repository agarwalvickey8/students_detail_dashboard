# Generated by Django 5.0.2 on 2024-05-04 13:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffsignup', '0007_remarkstudents_coachingroll'),
    ]

    operations = [
        migrations.CreateModel(
            name='NEETAdmitCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=252, null=True)),
                ('FatherName', models.CharField(blank=True, max_length=252, null=True)),
                ('DOB', models.DateField(blank=True, null=True)),
                ('NEETRoll', models.CharField(blank=True, max_length=252, null=True)),
                ('NEETApplication', models.CharField(blank=True, max_length=252, null=True)),
                ('Category', models.CharField(blank=True, max_length=252, null=True)),
                ('CentreNo', models.CharField(blank=True, max_length=252, null=True)),
                ('CentreName', models.TextField(blank=True, null=True)),
                ('CentreAddress', models.TextField(blank=True, null=True)),
                ('PWD', models.CharField(blank=True, max_length=252, null=True)),
                ('Stateofele', models.CharField(blank=True, max_length=252, null=True)),
                ('StudentDetail', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='staffsignup.studentdetails')),
            ],
            options={
                'verbose_name': 'NEET Admit Card Details',
                'verbose_name_plural': 'NEET Admit Card Details',
            },
        ),
    ]

# Generated by Django 5.0.2 on 2024-03-05 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffsignup', '0005_displaypreference_neetregisteration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neetregisteration',
            name='Mobile',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='neetregisteration',
            name='NEETApplication',
            field=models.BigIntegerField(),
        ),
    ]

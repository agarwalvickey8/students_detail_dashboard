# Generated by Django 5.0.2 on 2024-04-30 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffsignup', '0003_neetcityin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='neetcityin',
            options={'verbose_name': 'NEET City Intimation', 'verbose_name_plural': 'NEET City Intimation'},
        ),
        migrations.AddField(
            model_name='neetcityin',
            name='DOB',
            field=models.DateField(blank=True, null=True),
        ),
    ]

# Generated by Django 3.2.9 on 2021-12-16 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projekt', '0002_measurements_flow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='measurements',
            old_name='CO2',
            new_name='CO2_10000ppm',
        ),
        migrations.AddField(
            model_name='measurements',
            name='CO2_3000ppm',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

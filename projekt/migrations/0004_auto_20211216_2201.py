# Generated by Django 3.2.9 on 2021-12-16 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projekt', '0003_auto_20211216_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurements',
            name='Aeration_percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='measurements',
            name='Aeration',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='measurements',
            name='Feed',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='measurements',
            name='Mixer',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='measurements',
            name='Overflow',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='measurements',
            name='Recycle',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='measurements',
            name='Substrate',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
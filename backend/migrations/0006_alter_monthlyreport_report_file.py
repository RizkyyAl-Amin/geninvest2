# Generated by Django 5.1.3 on 2024-12-15 01:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_monthlyreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyreport',
            name='report_file',
            field=models.FileField(blank=True, help_text='Upload PDF laporan bulanan', null=True, upload_to='reports/', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]

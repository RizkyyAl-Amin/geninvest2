# Generated by Django 5.1.3 on 2024-12-14 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_stocktransaction_delete_rdntransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocktransaction',
            name='transaction_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]

# Generated by Django 5.0.3 on 2024-06-04 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_bids_is_valid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='is_valid',
            field=models.BooleanField(default=True),
        ),
    ]
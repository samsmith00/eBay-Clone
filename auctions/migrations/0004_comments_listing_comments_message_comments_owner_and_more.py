# Generated by Django 5.0.3 on 2024-05-31 19:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auction_listing_watch_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing', to='auctions.auction_listing'),
        ),
        migrations.AddField(
            model_name='comments',
            name='message',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comments',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='watch_list',
            field=models.ManyToManyField(blank=True, related_name='watch_list', to=settings.AUTH_USER_MODEL),
        ),
    ]

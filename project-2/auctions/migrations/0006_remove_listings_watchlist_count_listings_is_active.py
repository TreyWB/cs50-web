# Generated by Django 4.2.11 on 2024-09-16 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listings_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listings',
            name='watchlist_count',
        ),
        migrations.AddField(
            model_name='listings',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]

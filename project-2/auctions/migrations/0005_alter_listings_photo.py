# Generated by Django 4.2.11 on 2024-09-15 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_listing_listings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='photo',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

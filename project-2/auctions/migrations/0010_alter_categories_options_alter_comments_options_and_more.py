# Generated by Django 4.2.11 on 2024-09-17 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_listings_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name': 'Categories', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='comments',
            options={'verbose_name': 'Comments', 'verbose_name_plural': 'Comments'},
        ),
        migrations.AlterModelOptions(
            name='listings',
            options={'verbose_name': 'Listings', 'verbose_name_plural': 'Listings'},
        ),
        migrations.AlterModelOptions(
            name='winners',
            options={'verbose_name': 'Winners', 'verbose_name_plural': 'Winners'},
        ),
    ]

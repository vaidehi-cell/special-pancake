# Generated by Django 3.2.5 on 2022-06-18 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_alter_listing_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='pfp',
        ),
    ]
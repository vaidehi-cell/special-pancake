# Generated by Django 3.2.5 on 2022-06-18 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20220614_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pfp',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]

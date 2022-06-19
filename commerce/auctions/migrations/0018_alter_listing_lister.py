# Generated by Django 3.2.5 on 2022-06-18 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_user_pfp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='lister',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL),
        ),
    ]

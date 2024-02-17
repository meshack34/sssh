# Generated by Django 4.2.7 on 2024-01-16 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sub_part', '0017_accountentry_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountentry',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_accountentry', to=settings.AUTH_USER_MODEL),
        ),
    ]

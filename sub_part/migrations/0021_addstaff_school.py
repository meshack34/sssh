# Generated by Django 4.2.7 on 2024-01-22 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sub_part', '0020_alter_addincome_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='addstaff',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sub_part.school'),
        ),
    ]

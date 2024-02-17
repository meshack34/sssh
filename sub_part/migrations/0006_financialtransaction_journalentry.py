# Generated by Django 4.2.7 on 2024-01-08 12:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sub_part', '0005_remove_feestypediscount_fees_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('transaction_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sub_part.transactiontype')),
            ],
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debit_amount', models.FloatField()),
                ('credit_amount', models.FloatField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('gl_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sub_part.glline')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sub_part.financialtransaction')),
            ],
        ),
    ]

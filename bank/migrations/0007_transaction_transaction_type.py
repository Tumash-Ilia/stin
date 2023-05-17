# Generated by Django 4.2.1 on 2023-05-17 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0006_alter_account_balance_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw')], default='deposit', max_length=10),
        ),
    ]

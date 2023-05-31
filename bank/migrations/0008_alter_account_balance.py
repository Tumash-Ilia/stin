# Generated by Django 4.2.1 on 2023-05-31 13:03

from django.db import migrations
import djmoney.models.fields


def add_sample_data(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    SimpleModel = apps.get_model('bank', 'SimpleModel')
    SimpleModel.objects.create(just_text="Text 1")
    SimpleModel.objects.create(just_text="Text 2")


class Migration(migrations.Migration):
    dependencies = [
        ('bank', '0007_transaction_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='CZK', max_digits=10, null=True),
        ),
        migrations.RunPython(add_sample_data),
    ]
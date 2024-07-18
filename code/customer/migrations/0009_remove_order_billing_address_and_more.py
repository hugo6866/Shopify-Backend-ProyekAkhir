# Generated by Django 5.0.3 on 2024-07-17 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_discountcodecreationjob_discountcode_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='billing_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_title',
        ),
        migrations.AlterField(
            model_name='order',
            name='cancel_reason',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 5.0.3 on 2024-07-10 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_billing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

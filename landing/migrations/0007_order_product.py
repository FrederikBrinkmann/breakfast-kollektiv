# Generated by Django 5.1.2 on 2024-11-02 20:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0006_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, to='landing.product'),
            preserve_default=False,
        ),
    ]
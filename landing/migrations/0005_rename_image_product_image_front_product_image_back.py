# Generated by Django 5.1.2 on 2024-10-31 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0004_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image',
            new_name='image_front',
        ),
        migrations.AddField(
            model_name='product',
            name='image_back',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
    ]

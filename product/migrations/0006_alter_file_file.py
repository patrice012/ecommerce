# Generated by Django 4.1 on 2022-10-08 21:03

from django.db import migrations, models
import product.utils


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_product_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.ImageField(upload_to=product.utils.user_directory_path, verbose_name='Product Gallery'),
        ),
    ]

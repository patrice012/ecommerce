# Generated by Django 4.1 on 2022-10-06 21:02

from django.db import migrations, models
import product.utils


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='available',
            field=models.BooleanField(default=True, verbose_name='Available'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default='hello', max_length=50, verbose_name='Product name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(default=22, verbose_name='Price'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.FileField(default='h.jpg', upload_to=product.utils.upload_to, verbose_name='Product Gallery'),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.8 on 2023-12-21 11:18

import catalog.libs.db.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_productclass_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('structure', models.CharField(blank=True, choices=[('standalone', 'Standalone'), ('parent', 'Parent'), ('child', 'Child')], default='standalone', max_length=16)),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('upc', catalog.libs.db.fields.UpercasesCharField(blank=True, max_length=24, null=True, unique=True)),
                ('is_public', models.BooleanField(default=True)),
                ('slug', models.SlugField(default='SOME STRING', max_length=140)),
                ('meta_title', models.CharField(blank=True, max_length=128, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='catalog.product')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]

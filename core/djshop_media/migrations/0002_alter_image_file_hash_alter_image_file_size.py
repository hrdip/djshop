# Generated by Django 4.2.8 on 2023-12-21 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djshop_media', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file_hash',
            field=models.CharField(db_index=True, editable=False, max_length=40),
        ),
        migrations.AlterField(
            model_name='image',
            name='file_size',
            field=models.PositiveIntegerField(editable=False, null=True),
        ),
    ]

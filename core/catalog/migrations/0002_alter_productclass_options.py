# Generated by Django 4.2.8 on 2023-12-20 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productclass',
            name='options',
            field=models.ManyToManyField(blank=True, to='catalog.option'),
        ),
    ]
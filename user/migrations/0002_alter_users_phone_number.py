# Generated by Django 3.2.8 on 2023-10-28 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone_number',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]

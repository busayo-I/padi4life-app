# Generated by Django 3.2.8 on 2023-10-28 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_users_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone_number',
            field=models.BigIntegerField(null=True, unique=True),
        ),
    ]

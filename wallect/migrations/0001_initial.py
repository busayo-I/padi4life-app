# Generated by Django 3.2.8 on 2023-10-29 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('wallet_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('account_number', models.CharField(max_length=10, unique=True)),
                ('account_name', models.CharField(max_length=255)),
                ('pin', models.PositiveIntegerField()),
                ('bvn', models.CharField(blank=True, max_length=20, null=True)),
                ('currency', models.CharField(default='Naira', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

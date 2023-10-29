# Generated by Django 3.2.8 on 2023-10-29 20:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0006_alter_users_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='PadicoinAccount',
            fields=[
                ('account_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pin', models.PositiveIntegerField()),
                ('earned_today', models.DecimalField(decimal_places=2, max_digits=10)),
                ('last_activity_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.users')),
            ],
        ),
    ]
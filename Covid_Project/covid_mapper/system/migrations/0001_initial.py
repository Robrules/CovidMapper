# Generated by Django 3.2.8 on 2021-11-15 01:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('list_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('list_name', models.TextField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('street', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ListLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.list')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.location')),
            ],
        ),
    ]

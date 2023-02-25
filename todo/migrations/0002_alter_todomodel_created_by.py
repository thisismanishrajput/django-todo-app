# Generated by Django 4.1.6 on 2023-02-06 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todomodel',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todos', to=settings.AUTH_USER_MODEL),
        ),
    ]

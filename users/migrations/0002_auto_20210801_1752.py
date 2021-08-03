# Generated by Django 3.2.5 on 2021-08-01 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active_key',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='user',
            name='active_key_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

# Generated by Django 5.0.8 on 2024-08-09 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LoginSystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='access_token',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='access_token_created_at',
            field=models.DateTimeField(null=True),
        ),
    ]

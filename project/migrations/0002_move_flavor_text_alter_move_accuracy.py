# Generated by Django 5.1.3 on 2024-12-09 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='move',
            name='flavor_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='move',
            name='accuracy',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

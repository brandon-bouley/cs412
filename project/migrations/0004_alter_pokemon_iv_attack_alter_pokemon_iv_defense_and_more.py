# Generated by Django 5.1.3 on 2024-12-09 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_pokemon_ev_attack_pokemon_ev_defense_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='iv_attack',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='iv_defense',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='iv_health',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='iv_special_attack',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='iv_special_defense',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='iv_speed',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='moveset',
            field=models.ManyToManyField(related_name='used_by', to='project.move'),
        ),
    ]

# Generated by Django 4.2.1 on 2023-05-29 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_clone', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='paltform',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='watch_list', to='imdb_clone.streamplatform'),
            preserve_default=False,
        ),
    ]

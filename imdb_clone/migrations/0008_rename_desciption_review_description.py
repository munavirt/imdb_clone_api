# Generated by Django 4.1.7 on 2023-07-19 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_clone', '0007_rename_paltform_watchlist_platform'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='desciption',
            new_name='description',
        ),
    ]

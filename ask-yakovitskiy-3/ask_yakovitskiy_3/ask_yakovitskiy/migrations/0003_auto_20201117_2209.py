# Generated by Django 3.1.3 on 2020-11-17 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask_yakovitskiy', '0002_auto_20201117_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answers_number',
            field=models.IntegerField(default=0, verbose_name='Кол-во ответов'),
        ),
        migrations.AlterField(
            model_name='question',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рэйтинг'),
        ),
    ]

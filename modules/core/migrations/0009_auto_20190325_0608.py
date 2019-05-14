# Generated by Django 2.1.5 on 2019-03-25 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190325_0606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(blank=True, help_text='Максимальное кол-во символов: 250', max_length=250, null=True, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(blank=True, help_text='Максимальное кол-во символов: 250', max_length=250, null=True, verbose_name='Название жанра'),
        ),
    ]

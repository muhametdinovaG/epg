# Generated by Django 2.1.5 on 2019-02-25 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190219_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program', to='core.Provider', verbose_name='Поставщик'),
        ),
    ]
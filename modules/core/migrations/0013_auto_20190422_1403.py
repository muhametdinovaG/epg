# Generated by Django 2.1.5 on 2019-04-22 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20190422_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='channel', to='core.Provider'),
        ),
        migrations.AlterField(
            model_name='program',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='program', to='core.Category'),
        ),
        migrations.AlterField(
            model_name='program',
            name='channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='program', to='core.Channel'),
        ),
        migrations.AlterField(
            model_name='program',
            name='dvb_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='program', to='core.DvbGenre'),
        ),
        migrations.AlterField(
            model_name='program',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='program', to='core.Genre'),
        ),
    ]

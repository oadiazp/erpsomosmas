# Generated by Django 3.0.6 on 2020-08-06 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20200726_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='members', to='core.Club'),
        ),
    ]

# Generated by Django 3.0.5 on 2020-04-25 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200424_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='reference',
            field=models.CharField(default=-1, max_length=200),
            preserve_default=False,
        ),
    ]
# Generated by Django 3.0.5 on 2020-04-25 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_expense'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='fixed',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]

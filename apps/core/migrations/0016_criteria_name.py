# Generated by Django 3.0.6 on 2020-07-15 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20200712_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='criteria',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
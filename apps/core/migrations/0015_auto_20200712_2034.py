# Generated by Django 3.0.6 on 2020-07-12 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_profile_city'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MassMailCriteria',
            new_name='Criteria',
        ),
        migrations.AddField(
            model_name='massmail',
            name='criterias',
            field=models.ManyToManyField(to='core.Criteria'),
        ),
    ]
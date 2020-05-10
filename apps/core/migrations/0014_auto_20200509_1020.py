# Generated by Django 3.0.5 on 2020-05-09 10:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_massmail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='massmail',
            name='criteria',
        ),
        migrations.CreateModel(
            name='MassMailCriteria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('field', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('mass_mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.MassMail')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

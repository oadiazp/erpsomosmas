# Generated by Django 3.0.6 on 2020-05-10 13:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    replaces = [('core', '0013_massmail'), ('core', '0014_auto_20200509_1020')]

    dependencies = [
        ('core', '0012_auto_20200506_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='MassMail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
            ],
            options={
                'abstract': False,
            },
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

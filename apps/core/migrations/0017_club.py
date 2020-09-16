# Generated by Django 3.0.6 on 2020-07-25 18:32

import apps.core.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_criteria_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('coordinator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='coordinator', to='core.Profile')),
                ('criterias', models.ManyToManyField(to='core.Criteria')),
                ('members', models.ManyToManyField(related_name='club', to='core.Profile')),
            ],
            options={
                'abstract': False,
            },
            bases=(apps.core.models.FilterMixin, models.Model),
        ),
    ]
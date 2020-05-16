# Generated by Django 3.0.5 on 2020-05-06 22:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200503_1230'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='expense',
            name='kind',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.ExpenseKind'),
            preserve_default=False,
        ),
    ]
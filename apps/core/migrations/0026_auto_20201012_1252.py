# Generated by Django 3.0.6 on 2020-10-12 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_remove_criteria_mass_mails'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Donation',
        ),
        migrations.DeleteModel(
            name='Expense',
        ),
        migrations.DeleteModel(
            name='ExpenseKind',
        ),
    ]

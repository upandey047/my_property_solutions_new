# Generated by Django 3.2.7 on 2021-12-23 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0006_merge_20211217_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='renovation_required',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=5, verbose_name='Renovation Required'),
        ),
    ]

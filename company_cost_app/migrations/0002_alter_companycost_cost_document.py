# Generated by Django 5.1.1 on 2024-10-03 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_cost_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companycost',
            name='cost_document',
            field=models.FileField(blank=True, null=True, upload_to='company_cost_documents/'),
        ),
    ]

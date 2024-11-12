# Generated by Django 5.1.1 on 2024-10-01 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyDocumentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(blank=True, choices=[('license', 'Business License'), ('insurance', 'Insurance'), ('permits', 'Permits'), ('contracts', 'Contracts'), ('financial_statements', 'Financial Statements'), ('others', 'Others')], max_length=100, null=True)),
                ('document_name', models.CharField(blank=True, max_length=100, null=True)),
                ('document_number', models.CharField(blank=True, max_length=50, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('document_file', models.FileField(blank=True, null=True, upload_to='company_documents/')),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(blank=True, default=True, null=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('document_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_document', to='company_documentation_app.companydocumentcategory')),
            ],
        ),
    ]

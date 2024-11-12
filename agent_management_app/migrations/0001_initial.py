# Generated by Django 5.1.1 on 2024-10-01 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male', max_length=30)),
                ('agent_id', models.CharField(blank=True, max_length=50, null=True)),
                ('national_id', models.CharField(blank=True, max_length=50, null=True)),
                ('visa_rate', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('emergency_contact_number', models.CharField(blank=True, max_length=20, null=True)),
                ('note', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.TextField(blank=True, max_length=254, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='agents/')),
                ('status', models.BooleanField(blank=True, default=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AgentDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_name', models.CharField(blank=True, max_length=256, null=True)),
                ('document_type', models.CharField(blank=True, choices=[('pdf', 'Pdf'), ('image', 'Image'), ('word', 'Word')], max_length=20, null=True)),
                ('document_file', models.FileField(blank=True, null=True, upload_to='agent_documents/')),
                ('document_description', models.TextField(blank=True, null=True)),
                ('collected_data', models.DateField(blank=True, null=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('expiry_days', models.IntegerField(blank=True, default=0, null=True)),
                ('document_statu', models.BooleanField(blank=True, default=True, null=True)),
                ('creation_date', models.DateField(auto_now_add=True, null=True)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_document', to='agent_management_app.agentinfo')),
            ],
        ),
        migrations.CreateModel(
            name='AgentAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent_payable', models.FloatField(blank=True, default=0.0, null=True)),
                ('agent_total_credit', models.FloatField(blank=True, default=0.0, null=True)),
                ('agent_total_debit', models.FloatField(blank=True, default=0.0, null=True)),
                ('opening_balance', models.FloatField(blank=True, default=0.0, null=True)),
                ('previous_balance', models.FloatField(blank=True, default=0.0, null=True)),
                ('total_balance', models.FloatField(blank=True, default=0.0, null=True)),
                ('is_credit', models.BooleanField(blank=True, default=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('account_status', models.BooleanField(blank=True, default=True, null=True)),
                ('open_date', models.DateField(auto_now_add=True, null=True)),
                ('agent', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_account', to='agent_management_app.agentinfo')),
            ],
        ),
        migrations.CreateModel(
            name='AgentTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(blank=True, choices=[('Cash', 'Cash Payment'), ('Bank', 'Bank Transfer'), ('Online', 'Online Payment')], default='Cash', max_length=10, null=True)),
                ('note', models.CharField(blank=True, max_length=100, null=True)),
                ('online_transaction_number', models.CharField(blank=True, max_length=50, null=True)),
                ('online_transaction_file', models.FileField(blank=True, null=True, upload_to='agent_online_transaction_file/')),
                ('bank_transaction_number', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_transaction_file', models.FileField(blank=True, null=True, upload_to='agent_bank_transaction_file/')),
                ('balance', models.FloatField(blank=True, default=0.0, null=True)),
                ('credit', models.FloatField(blank=True, default=0.0, null=True)),
                ('debit', models.FloatField(blank=True, default=0.0, null=True)),
                ('transaction_hold_status', models.BooleanField(blank=True, default=False, null=True)),
                ('payment_transaction_id', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('payment_status', models.BooleanField(blank=True, default=True, null=True)),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('agent_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_account', to='agent_management_app.agentaccount')),
            ],
        ),
    ]
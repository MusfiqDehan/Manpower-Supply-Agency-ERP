# Generated by Django 5.1.1 on 2024-10-01 09:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agent_management_app', '0001_initial'),
        ('visa_management_app', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('passport_date_of_expairy', models.DateField(blank=True, null=True)),
                ('full_name', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=30, null=True)),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Birth date')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Phone number')),
                ('address', models.TextField(blank=True, max_length=254, null=True, verbose_name='Address')),
                ('emergency_contact_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='emergency contact number')),
                ('passenger_image', models.FileField(blank=True, null=True, upload_to='', verbose_name='passenger_image/')),
                ('fly_status', models.BooleanField(blank=True, default=False, null=True)),
                ('cancel_status', models.BooleanField(blank=True, default=False, null=True)),
                ('money_refund_status', models.BooleanField(blank=True, default=False, null=True)),
                ('status', models.BooleanField(blank=True, default=True, null=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('agent_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passenger_agent', to='agent_management_app.agentinfo')),
            ],
        ),
        migrations.CreateModel(
            name='PassengerDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_name', models.CharField(blank=True, choices=[('passport_received', 'Passport Received Status'), ('police_clearance', 'Police Clearance Status'), ('medical_certificate', 'Medical Certificate Status'), ('mofa_status', 'MOFA Status'), ('finger_appointment', 'Finger Appointment Status'), ('visa_status', 'Visa Status'), ('training_status', 'Training Status'), ('finger_status', 'Finger Status'), ('manpower_status', 'Manpower Status'), ('ticket_status', 'Ticket Status'), ('flight', 'Flight Status')], max_length=50, null=True)),
                ('document_type', models.CharField(blank=True, choices=[('pdf', 'Pdf'), ('image', 'Image'), ('word', 'Word')], default='pdf', max_length=20, null=True)),
                ('document_file', models.FileField(blank=True, null=True, upload_to='passenger_documents/')),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('collected_data', models.DateField(blank=True, null=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('expiry_days', models.IntegerField(blank=True, default=0, null=True)),
                ('status', models.BooleanField(blank=True, default=True, null=True)),
                ('creation_date', models.DateField(auto_now_add=True, null=True)),
                ('flight_date', models.DateField(blank=True, null=True)),
                ('passenger', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passenger_document', to='passenger_app.passenger')),
                ('visa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='visa', to='visa_management_app.visa')),
            ],
        ),
        migrations.CreateModel(
            name='PassengerGeneralDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_name', models.CharField(blank=True, max_length=100, null=True)),
                ('document_type', models.CharField(blank=True, choices=[('pdf', 'Pdf'), ('image', 'Image'), ('word', 'Word')], default='pdf', max_length=20, null=True)),
                ('document_file', models.FileField(blank=True, null=True, upload_to='passenger_general_documents/')),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('creation_date', models.DateField(auto_now_add=True, null=True)),
                ('passenger', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passenger_general_document', to='passenger_app.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='PassengerPassport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport_number', models.CharField(blank=True, max_length=50, null=True)),
                ('date_of_expairy', models.DateField(blank=True, null=True)),
                ('passport_scanned_image', models.FileField(blank=True, null=True, upload_to='', verbose_name='passenger_passport_image/')),
                ('passport_received', models.BooleanField(blank=True, default=False, null=True)),
                ('police_clearance', models.BooleanField(blank=True, default=False, null=True)),
                ('medical_certificate', models.BooleanField(blank=True, default=False, null=True)),
                ('mofa_status', models.BooleanField(blank=True, default=False, null=True)),
                ('finger_appointment', models.BooleanField(blank=True, default=False, null=True)),
                ('visa_status', models.BooleanField(blank=True, default=False, null=True)),
                ('training_status', models.BooleanField(blank=True, default=False, null=True)),
                ('finger_status', models.BooleanField(blank=True, default=False, null=True)),
                ('manpower_status', models.BooleanField(blank=True, default=False, null=True)),
                ('ticket_status', models.BooleanField(blank=True, default=False, null=True)),
                ('last_update', models.DateTimeField(auto_now=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('passenger_passport', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passport_info_passenger', to='passenger_app.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='PassengerTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_balance', models.FloatField(blank=True, default=0.0, null=True)),
                ('credit', models.FloatField(blank=True, default=0.0, null=True)),
                ('debit', models.FloatField(blank=True, default=0.0, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('payment_transaction_id', models.CharField(blank=True, max_length=20, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('transaction_date', models.DateField(blank=True, null=True)),
                ('passenger', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passenger_account', to='passenger_app.passenger')),
            ],
        ),
    ]

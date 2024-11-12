from django.db import models



# Create your models here.
class Visa(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True) 
    visa_id = models.CharField(max_length=255, blank=True, null=True) 
    sponsor_id = models.CharField(max_length=255, blank=True, null=True) 
    number_of_visa = models.IntegerField(blank=True, null=True)
    office = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    
    collected_data = models.DateField(null=True, blank=True)
    expiry_date=models.DateField(null=True, blank=True)
    expiry_days = models.IntegerField(blank=True, null=True, default=0)
    file = models.FileField(upload_to='visa_documents/', blank=True, null=True)
    status = models.BooleanField(default=True, blank=True, null= True)
    reference = models.CharField(max_length=256, blank=True, null=True) 
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
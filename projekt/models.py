from django.db import models
from django.utils import timezone
import datetime
# Create your models here.
class Measurements(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False) 
    
    Level = models.FloatField(blank=True, null=True)
    Aeration = models.BooleanField(default=True)
    Feed = models.BooleanField(default=True)
    Mixer = models.BooleanField(default=True)
    Overflow = models.BooleanField(default=True)
    Recycle = models.BooleanField(default=True)
    Substrate = models.BooleanField(default=True)
    CO2 = models.FloatField(blank=True, null=True)
    Mixing = models.FloatField(blank=True, null=True)
    pH = models.FloatField(blank=True, null=True)
    Temperature = models.FloatField(blank=True, null=True)
    Redox = models.FloatField(blank=True, null=True)
    Turbidity = models.FloatField(blank=True, null=True)
    Oxygen = models.FloatField(blank=True, null=True)
    Flow = models.FloatField(blank=True, null=True)

    timestamp = models.DateTimeField('Created Time', auto_now=True, null=True)

    class Meta:
        managed = True
        db_table = 'Measurements'

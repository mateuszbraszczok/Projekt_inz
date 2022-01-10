from django.db import models
from django.utils import timezone
import datetime
# Create your models here.

class Measurements(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False) 
    Aeration = models.BooleanField(blank=True, null=True)
    Feed = models.BooleanField(blank=True, null=True)
    Mixer = models.BooleanField(blank=True, null=True)
    Overflow = models.BooleanField(blank=True, null=True)
    Recycle = models.BooleanField(blank=True, null=True)
    Substrate = models.BooleanField(blank=True, null=True)
    CO2_3000ppm = models.FloatField(blank=True, null=True)
    CO2_10000ppm = models.FloatField(blank=True, null=True)
    Aeration_percentage = models.FloatField(blank=True, null=True)
    Mixing = models.FloatField(blank=True, null=True)
    Level = models.FloatField(blank=True, null=True)
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

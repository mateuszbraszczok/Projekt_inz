from django.db import models

# Create your models here.
class Measurements(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    poziom = models.FloatField(blank=True, null=True)
    natlenienie = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(db_column='Timestamp', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Measurements'
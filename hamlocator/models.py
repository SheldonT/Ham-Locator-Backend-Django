# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import uuid
from django.db import models


class Logs(models.Model):
    record_id = models.CharField(primary_key=True, max_length=255, default=uuid.uuid4)
    user_id = models.CharField(max_length=255, blank=False, null=False)
    contact_call = models.CharField(max_length=255, blank=False, null=False)
    freq = models.FloatField(blank=False, null=False)
    mode = models.CharField(max_length=255, blank=False, null=False)
    sig_rep_sent = models.IntegerField(blank=True, null=True)
    sig_rep_recv = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    grid = models.CharField(max_length=255, blank=True, null=True)
    serial_sent = models.IntegerField(blank=True, null=True)
    serial_recv = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    details = models.CharField(max_length=255, blank=True, null=True)
    contact_date = models.DateField(blank=False, null=False)
    contact_time = models.TimeField(blank=False, null=False)
    utc = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logs'


class Session(models.Model):
    sid = models.CharField(primary_key=True)
    sess = models.TextField()  # This field type is a guess.
    expire = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'session'

class Users(models.Model):
    userid = models.CharField(primary_key=True, max_length=255)
    callsign = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    gridloc = models.CharField(max_length=255, blank=True, null=True)
    privilege = models.CharField(max_length=255, blank=True, null=True)
    units = models.CharField(max_length=255, blank=True, null=True)
    itu = models.IntegerField(blank=True, null=True)
    utc = models.FloatField(blank=True, null=True)
    #passwd = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
        unique_together = (('callsign', 'email'),)

    @classmethod
    def get_custom_claims(cls, include_system_fields=False):

        #define the system fields that are not custom claims
        if include_system_fields:
            system_fields = []
        else:       
            system_fields = [
                'userid', 'email'
            ]
        
        #define the custom claims by excluding system fields
        claims = [field.name for field in cls._meta.fields if field.name not in system_fields]

        return claims
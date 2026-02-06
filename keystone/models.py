from django.db import models


# class Users(models.Model):
#     userid = models.CharField(primary_key=True, max_length=255)
#     callsign = models.CharField(max_length=255, blank=True, null=True)
#     email = models.CharField(max_length=255, blank=True, null=True)
#     country = models.CharField(max_length=255, blank=True, null=True)
#     lat = models.FloatField(blank=True, null=True)
#     lng = models.FloatField(blank=True, null=True)
#     gridloc = models.CharField(max_length=255, blank=True, null=True)
#     privilege = models.CharField(max_length=255, blank=True, null=True)
#     units = models.CharField(max_length=255, blank=True, null=True)
#     itu = models.IntegerField(blank=True, null=True)
#     utc = models.FloatField(blank=True, null=True)
#     #passwd = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'users'
#         unique_together = (('callsign', 'email'),)

#     @classmethod
#     def get_custom_claims(cls, include_system_fields=False):

#         #define the system fields that are not custom claims
#         if include_system_fields:
#             system_fields = []
#         else:       
#             system_fields = [
#                 'userid', 'email'
#             ]
        
#         #define the custom claims by excluding system fields
#         claims = [field.name for field in cls._meta.fields if field.name not in system_fields]

#         return claims
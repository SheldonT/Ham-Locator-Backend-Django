# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import re
import uuid
import plistlib
import unicodedata
from functools import lru_cache
from datetime import datetime
from math import asin, cos, radians, sin, sqrt
from zoneinfo import ZoneInfo

import maidenhead as mh
from django.apps import apps
from django.db import models
import requests
from timezonefinder import TimezoneFinder


TIMEZONE_FINDER = TimezoneFinder()
COUNTRY_FILES_CTY_URL = 'https://www.country-files.com/cty/cty.plist'


@lru_cache(maxsize=1)
def _load_country_files_entities():
    response = requests.get(COUNTRY_FILES_CTY_URL, timeout=20)
    response.raise_for_status()
    return plistlib.loads(response.content)


def _haversine_distance_km(lat1, lng1, lat2, lng2):
    earth_radius_km = 6371.0
    lat1_rad = radians(lat1)
    lng1_rad = radians(lng1)
    lat2_rad = radians(lat2)
    lng2_rad = radians(lng2)

    delta_lat = lat2_rad - lat1_rad
    delta_lng = lng2_rad - lng1_rad
    a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lng / 2) ** 2
    return 2 * earth_radius_km * asin(sqrt(a))


def _decode_escaped_unicode(value):
    if not isinstance(value, str):
        return value

    # Decode only when escaped sequences are present.
    if '\\u' not in value and '\\U' not in value:
        return value

    try:
        return value.encode('utf-8').decode('unicode_escape')
    except UnicodeDecodeError:
        return value


def _country_from_coordinates(lat, lng):
    if lat is None or lng is None:
        return None

    app_config = apps.get_app_config('hamlocator')
    geolocator = getattr(app_config, 'geolocator', None)
    if geolocator is None:
        return None

    try:
        # Force English country names regardless of server/browser locale.
        address = geolocator.reverse(f"{lat}, {lng}", language='en')
    except Exception:
        return None

    if address is None:
        return None

    raw_address = getattr(address, 'raw', {}) or {}
    address_fields = raw_address.get('address', {}) or {}
    country = address_fields.get('country')

    if not country:
        country_parts = str(address).split(',')
        country = country_parts[-1].strip() if country_parts else None

    return country


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

    # def _normalize_text_fields(self):
    #     text_fields = [
    #         'contact_call',
    #         'mode',
    #         'name',
    #         'grid',
    #         'comment',
    #         'country',
    #         'details',
    #     ]

    #     for field_name in text_fields:
    #         field_value = getattr(self, field_name, None)
    #         if isinstance(field_value, str):
    #             setattr(self, field_name, _decode_escaped_unicode(field_value))

    # def save(self, *args, **kwargs):
    #     # Logs should preserve client-supplied values, including country.
    #     self._normalize_text_fields()
    #     super().save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'logs'


class Session(models.Model):
    sid = models.CharField(primary_key=True)
    sess = models.TextField()  # This field type is a guess.
    expire = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'session'

class Users(models.Model):
    uid = models.CharField(primary_key=True, max_length=255, db_column='userid')
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
        managed = True
        db_table = 'users'
        unique_together = (('callsign', 'email'),)

    @staticmethod
    def _normalize_text(value):
        if value is None:
            return ''
        normalized = unicodedata.normalize('NFKD', str(value))
        normalized = normalized.encode('ascii', 'ignore').decode('ascii')
        return re.sub(r'[^a-z0-9]+', '', normalized.casefold())

    def _set_coordinates_from_grid(self):
        if not self.gridloc:
            return

        try:
            self.lat, self.lng = mh.to_location(self.gridloc)
        except Exception:
            self.lat = 1
            self.lng = 1

    def _set_country_from_coordinates(self):
        country = _country_from_coordinates(self.lat, self.lng)
        if country:
            self.country = country

    def _set_itu_from_coordinates(self):
        if self.lat is None or self.lng is None:
            return

        try:
            entities = _load_country_files_entities()
        except Exception:
            return

        target_country = self._normalize_text(self.country)
        best_entity = None
        best_distance = None

        for entity in entities.values():
            entity_itu = entity.get('ITUZone')
            entity_lat = entity.get('Latitude')
            entity_lng = entity.get('Longitude')
            if entity_itu is None or entity_lat is None or entity_lng is None:
                continue

            if target_country:
                normalized_entity_country = self._normalize_text(entity.get('Country'))
                if not (
                    normalized_entity_country == target_country
                    or normalized_entity_country in target_country
                    or target_country in normalized_entity_country
                ):
                    continue

            distance = _haversine_distance_km(self.lat, self.lng, entity_lat, entity_lng)
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_entity = entity

        if best_entity is None and target_country:
            for entity in entities.values():
                entity_itu = entity.get('ITUZone')
                entity_lat = entity.get('Latitude')
                entity_lng = entity.get('Longitude')
                if entity_itu is None or entity_lat is None or entity_lng is None:
                    continue

                distance = _haversine_distance_km(self.lat, self.lng, entity_lat, entity_lng)
                if best_distance is None or distance < best_distance:
                    best_distance = distance
                    best_entity = entity

        if best_entity and best_entity.get('ITUZone') is not None:
            self.itu = int(best_entity['ITUZone'])

    def _set_utc_from_coordinates(self):
        if self.lat is None or self.lng is None:
            return

        timezone_name = TIMEZONE_FINDER.timezone_at(lat=self.lat, lng=self.lng)
        if not timezone_name:
            return

        try:
            offset = datetime.now(ZoneInfo(timezone_name)).utcoffset()
        except Exception:
            return

        if offset is not None:
            self.utc = -1 * offset.total_seconds() / 3600

    def _normalize_text_fields(self):
        text_fields = [
            'uid',
            'callsign',
            'email',
            'country',
            'gridloc',
            'privilege',
            'units',
        ]

        for field_name in text_fields:
            field_value = getattr(self, field_name, None)
            if isinstance(field_value, str):
                setattr(self, field_name, _decode_escaped_unicode(field_value))

    def save(self, *args, **kwargs):
        self._normalize_text_fields()
        self._set_coordinates_from_grid()
        self._set_country_from_coordinates()
        self._set_itu_from_coordinates()
        self._set_utc_from_coordinates()

        super().save(*args, **kwargs)

    @classmethod
    def get_custom_claims(cls, include_system_fields=False):

        #define the system fields that are not custom claims
        if include_system_fields:
            system_fields = []
        else:       
            system_fields = [
                'uid', 'email'
            ]
        
        #define the custom claims by excluding system fields
        claims = [field.name for field in cls._meta.fields if field.name not in system_fields]

        return claims
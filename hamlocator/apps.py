from django.apps import AppConfig
from geopy.geocoders import Nominatim
from pyhamtools import LookupLib, Callinfo

class HamlocatorConfig(AppConfig):
    name = 'hamlocator'

    # This placeholder holds our instance
    geolocator = None

    cic = None

    def ready(self):
        # This code runs exactly once when Django completely loads this app
        self.geolocator = Nominatim(user_agent="self.name")

        lookup_db = LookupLib(lookuptype="countryfile")
        self.cic = Callinfo(lookup_db)

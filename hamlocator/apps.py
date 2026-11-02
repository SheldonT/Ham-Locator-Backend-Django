from django.apps import AppConfig
from geopy.geocoders import Nominatim
from pyhamtools import LookupLib, Callinfo
import logging

logger = logging.getLogger(__name__)

class HamlocatorConfig(AppConfig):
    name = 'hamlocator'

    # This placeholder holds our instance
    geolocator = None

    cic = None

    def ready(self):
        # This code runs exactly once when Django completely loads this app
        self.geolocator = Nominatim(user_agent="self.name")

        try:
            lookup_db = LookupLib(lookuptype="countryfile")
            self.cic = Callinfo(lookup_db)
        except KeyError as e:
            logger.warning(f"Failed to initialize country lookup database: {e}. "
                          "This may be due to outdated country data in pyhamtools. "
                          "Country lookups will not be available.")
            self.cic = None

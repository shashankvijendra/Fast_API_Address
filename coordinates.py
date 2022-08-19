"""
file : coordinates.py
Description :  Fetch the address based on coordinates using geopy module
Author : Shashank.V
"""

from geopy.geocoders import Nominatim

def location_address(start):
    """
        Fetch the address based on coordinates using geopy module
    """
    try:
        geolocator = Nominatim(user_agent="app")
        location = geolocator.reverse(start)
        return location.address
    except Exception:
        return False

# print(location_address("100.289261320717177, 10.63414484755613"))
# location_address("12.289261320717177, 76.63414484755613")
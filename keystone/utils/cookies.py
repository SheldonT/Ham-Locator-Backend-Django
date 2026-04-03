from django.conf import settings
from google_crc32c import value

def set_auth_cookie(response, name, value, max_age=None):
    """
    Set a cookie with HttpOnly and Secure flags for cross-site usage.
    """
    response.set_cookie(
        name,
        value,
        max_age=max_age,
        httponly=True,
        secure=True,  # Required for SameSite=None
        samesite='None',  # Allow cross-site cookie usage
        path='/'
    )

def delete_auth_cookie(response, name):
    """
    Delete a cookie by setting its max_age to 0.
    """
    response.delete_cookie(name)

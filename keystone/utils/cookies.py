from django.conf import settings

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
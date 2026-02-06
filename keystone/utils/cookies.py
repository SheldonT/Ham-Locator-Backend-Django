from django.conf import settings

def set_auth_cookie(response, name, value, max_age=None):
    """
    Set a cookie with HttpOnly and Secure flags.
    """
    response.set_cookie(
        name,
        value,
        max_age=max_age,
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax' if settings.DEBUG else 'Strict',
        path='/'
    )
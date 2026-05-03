
# Keystone Django App

A reusable Django app for authentication and user management.

## Installation

```bash
pip install keystone-django
```

## Usage

Add `keystone` to your `INSTALLED_APPS` in Django settings:

```python
INSTALLED_APPS = [
	# ...existing apps...
	'keystone',
]
```

### Required settings.py Variables

#### Email Settings (for Password Reset)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yourprovider.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your@email.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'your@email.com'
```


#### Keystone-specific Settings (Firebase Only)

> **Note:** Currently, only Firebase is supported as an authentication provider.

```python
# Firebase settings (required)
FIREBASE_API_KEY = 'your-firebase-api-key'
FIREBASE_AUTH_DOMAIN = 'your-firebase-auth-domain'
FIREBASE_PROJECT_ID = 'your-firebase-project-id'

# Password reset URL (used in email templates)
PASSWORD_RESET_URL = 'https://yourdomain.com/reset-password/{token}/'


# Optional Keystone settings
#
# Use Firebase password reset (default: None)
USE_FIREBASE_PW_RESET = True
#
# Override the default Firebase password reset API endpoint (default: None)
# FIREBASE_PW_RESET_API = 'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key=...'
#
# Custom password reset URL for emails (default: None)
# KEYSTONE_CUSTOM_PASSWORD_RESET_URL = 'https://yourdomain.com/custom-reset/{token}/'
#
# Custom user model (default: None)
# KEYSTONE_USER_MODEL = 'yourapp.CustomUser'
```

> ⚠️ **Note:** Adjust the above variables to match your environment and provider. Check the `keystone` documentation or code for additional required settings.

## Development

- Build: `python -m build`
- Install locally: `pip install dist/keystone_django-<version>-py3-none-any.whl`

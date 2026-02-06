from django.conf import settings
from django.apps import apps

def get_user_model():
    """
    Returns the User model that is active in this project.
    """

    model = getattr(settings, "KEYSTONE_USER_MODEL", None)
    model_parts= model.split('.')

    app_label = model_parts[0]
    model_name = model_parts[-1]
    
    model = apps.get_model(app_label, model_name)

    return model
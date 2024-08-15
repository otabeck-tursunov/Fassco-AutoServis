from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainApp'

    verbose_name = _('Storage')


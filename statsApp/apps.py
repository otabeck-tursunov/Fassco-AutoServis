from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StatsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'statsApp'

    verbose_name = _('Commerce')

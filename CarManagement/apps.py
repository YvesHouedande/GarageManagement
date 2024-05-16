from django.apps import AppConfig
from django.core.signals import request_finished


class CarmanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CarManagement'
    
    def ready(self):
        from  .import signals
        # request_finished.connect(signals.create_entre_panne)

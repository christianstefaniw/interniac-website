from django.apps import AppConfig


class MarketplaceConfig(AppConfig):
    name = 'marketplace'

    def ready(self):
        import marketplace.signals
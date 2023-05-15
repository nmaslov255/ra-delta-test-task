from django.core.management import BaseCommand
from django.core.cache import cache

from api.tasks import calculate_delivery_prices


class Command(BaseCommand):
    help = "This command update delivery price for unprocessed packages"

    def handle(self, *args, **kwargs):
        result = calculate_delivery_prices.apply_async(countdown=1)
        self.stdout.write(f'Task id={result.id} was called')
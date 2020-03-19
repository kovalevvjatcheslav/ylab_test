from django.core.management.base import BaseCommand, CommandError
from api.tasks import update_rate


class Command(BaseCommand):

    def handle(self, *args, **options):
        update_rate()

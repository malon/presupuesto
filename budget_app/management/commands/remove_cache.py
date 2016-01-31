# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from budget_app.management import CacheRemover


class Command(BaseCommand):
    help = u"Elimina la cache a disco, obligando a recargar de nuevo las páginas."

    def handle(self, *args, **options):
        CacheRemover().remove()

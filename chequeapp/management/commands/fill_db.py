import os
import json

from django.core.management import BaseCommand

from chequeapp.models import Printer

JSON_PATH = 'chequeapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    """fixtures для модели Printer"""
    def handle(self, *args, **options):
        printers = load_from_json('printer_db')
        Printer.objects.all().delete()
        for printer in printers:
            new_printer = Printer(**printer)
            new_printer.save()

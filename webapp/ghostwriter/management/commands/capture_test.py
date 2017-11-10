from __future__ import absolute_import
from django.core.management.base import BaseCommand
from datetime import datetime
from time import sleep


class PersistentProcess(object):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("PROCESS END")
        return True

    def run(self):
        while True:
            print(datetime.now())
            sleep(30)


class Command(BaseCommand):
    help = "Test command for asynchronous capture"

    def handle(self, *args, **options):
        with PersistentProcess() as p:
            p.run()

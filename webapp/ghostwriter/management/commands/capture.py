from __future__ import absolute_import
from django.core.management.base import BaseCommand
from slidecapture import SlideCapture, SlideCaptureError


class Command(BaseCommand):
    help = "Capturing slides"

    def handle(self, *args, **options):
        try:
            with SlideCapture(0) as cap:
                cap.monitor_slides("media/cache")
        except SlideCaptureError:
            print("Couldn't open camera!!")

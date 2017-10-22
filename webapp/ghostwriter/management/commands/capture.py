from __future__ import absolute_import
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from .slidecapture import SlideCapture, SlideCaptureError


class Command(BaseCommand):
    help = "Capturing slides"

    def handle(self, *args, **options):
        try:
            with SlideCapture(1) as cap:
                cap.monitor_slides("media/cache")
        except SlideCaptureError:
            pass

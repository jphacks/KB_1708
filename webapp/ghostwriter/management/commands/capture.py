from __future__ import absolute_import
from django.core.management.base import BaseCommand
from ghostwriter.capture_lib.slidecapture import SlideCapture, SlideCaptureError


class Command(BaseCommand):
    help = "Capturing slides"

    def add_arguments(self, parser):
        parser.add_argument('skip_frame_num',
                            type=int,
                            help='Skip frame number',
                            default=3,
                            nargs="?")

    def handle(self, *args, **options):
        try:
            with SlideCapture(0) as cap:
                cap.monitor_slides("media/cache", options['skip_frame_num'])
        except SlideCaptureError:
            print("Couldn't open camera!!")

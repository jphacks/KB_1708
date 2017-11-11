from __future__ import absolute_import
import os
from logging import getLogger
from django.conf import settings
from django.core.management.base import BaseCommand
from slidecapture import SlideCapture


class Command(BaseCommand):
    help = "Capture slides from video file."

    def add_arguments(self, parser):
        parser.add_argument('video_file',
                            type=str,
                            help='Specify your video file name under the images directory')

    def handle(self, *args, **options):
        logger = getLogger("CaptureTest")
        video_file = options['video_file']
        video_dir = os.path.join(settings.MEDIA_ROOT, "images")
        save_dir = os.path.join(settings.MEDIA_ROOT, "cache")
        video_path = os.path.join(video_dir, video_file)
        if not os.path.exists(video_path):
            logger.exception("{}: Could not found".format(video_path))
            exit(1)
        with SlideCapture(video_path, is_debug=True) as cap:
            cap.monitor_slides(save_dir)

from __future__ import absolute_import
import os
from logging import getLogger, basicConfig, INFO
from django.conf import settings
from datetime import datetime
from django.core.files import File
from django.core.management.base import BaseCommand
from ghostwriter.models import Image
from ghostwriter.tasks import check_file


class Command(BaseCommand):
    help = "Capture slides from video file."

    def handle(self, *args, **options):
        logger = getLogger("AddImages")
        basicConfig(level=INFO)
        files = check_file("media/cache", ".jpg")
        now = datetime.now()
        cache_dir = os.path.join(settings.MEDIA_ROOT, 'cahche')
        for i, file in enumerate(files):
            image_path = os.path.join(cache_dir, file)
            with open(image_path, "rb") as jpg:
                django_file = File(jpg)
                img = Image()
                img.image.save(now.strftime("%Y-%m-%d %H:%M:%S") + "-" + str(i) + ".jpg", django_file, save=True)
                img.title = now.strftime("%Y-%m-%d %H:%M:%S") + "-" + str(i)
                img.save()
                logger.info("Register: {}".format(file))
            os.remove(image_path)

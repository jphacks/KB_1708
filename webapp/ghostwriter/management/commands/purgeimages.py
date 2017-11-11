from __future__ import absolute_import
from logging import getLogger, basicConfig, INFO
from django.core.management.base import BaseCommand
from ghostwriter.models import Lecture


class Command(BaseCommand):
    help = "Capture slides from video file."

    def add_arguments(self, parser):
        parser.add_argument('lecture', type=str, help='Specify lecture name')

    def handle(self, *args, **options):
        logger = getLogger("AddImages")
        basicConfig(level=INFO)
        lec_title = options['lecture']
        lectures = Lecture.objects.filter(title=lec_title).all()
        if len(lectures) == 0:
            logger.exception('{}: No such lecture'.format(lec_title))
            exit(1)
        else:
            logger.info("Found: {}".format(str([l.title for l in lectures])))
        for lecture in lectures:
            related_images = lecture.images.all()
            for image in related_images:
                lecture.images.remove(image)
                logger.info("Purge: {}".format(image.title))
            lecture.ocr_text = ""
            lecture.save()

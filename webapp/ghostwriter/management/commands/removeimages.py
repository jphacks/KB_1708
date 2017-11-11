from __future__ import absolute_import
import os
from logging import getLogger, basicConfig, INFO
from django.core.management.base import BaseCommand
from ghostwriter.models import Image


class Command(BaseCommand):
    help = "Remove registered images"

    def add_arguments(self, parser):
        parser.add_argument('--remove',
                            dest="remove",
                            default=False,
                            action='store_true',
                            help='Remove image file from media directory')

    def handle(self, *args, **options):
        logger = getLogger('RemoveImages')
        basicConfig(level=INFO)
        images = Image.objects.all()
        path_list = list()
        for image in images:
            logger.info('Remove: {}'.format(image.title))
            path_list.append(image.image.path)
            image.delete()
        if options['remove']:
            for path in path_list:
                os.remove(path)
